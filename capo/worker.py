import json
import time
import datetime

from models import Job as JobDB
from models import Log, Worker
from models import FAILED, WAITING, RUNNING, COMPLETED, load_action

from settings import ACTIONS


def execute(action_name, action_param):
    action = load_action(ACTIONS, action_name)()
    action.run(action_param)
    return action


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.timedelta):
        "return total number of minutes"
        return "%.2f" % obj.total_seconds() / 60

    if isinstance(obj, datetime.datetime):
        return str(obj)


class Logger(object):
    def log(self, code, job_id, msg):
        print msg
        return Log.objects.create(**dict(
            job_id=job_id,
            msg=msg,
            code=code
        ))


class Worker(object):
    jobs = []
    runing_jobs = []
    current_job = None
    status = WAITING

    def run_job(self, job_id, job_param=None):
        task_list = []

        job = JobDB.objects.get(pk=job_id)

        job_param = json.loads(job.param)
        job_param['job_id'] = job.id
        job_param['started_at'] = job.started_at

        job.started_at = datetime.datetime.now()
        job.save()
        
        self.current_job = job
        self.jobs.append(job)
        self.status = RUNNING

        job_tasks = job.recipe.task_set.all().order_by("order")
        for job_task in job_tasks:
            task_list.append(dict(
                action_name=job_task.action_name,
                action_param=job_task.param,
                on_error_action_name=job_task.on_error_action,
                on_error_action_param=job_task.on_error_param,
                repeated_param=job_task.repeated_run_param,
            ))

        new_job = Job(job_param, task_list)
        new_job.run()

        job.completed_at = new_job.completed_at
        job.status = new_job.status
        job.save()


class Job(object):
    """docstring for RunJob"""
    job_id = None
    job_param = {}
    original_task_list = []
    completed_at = None
    status = RUNNING
    logger = Logger()

    def __init__(self, job_param, task_list):
        self.job_param = job_param
        self.job_id = job_param["job_id"]
        self.original_task_list = task_list

    def log(self, code, msg):
        self.logger.log(code, self.job_id, msg)

    def run(self):
        completed, job_param = self.do_tasks(self.job_param, self.original_task_list)
        if completed:
            self.status = 3
            self.completed_at = datetime.datetime.now()
            self.result = json.dumps(job_param, default=json_serial)
        else:
            self.status = 0

    def do_task(self, action_name, action_param, job_param):
        """
        Run the task
        param: action_param - the param that can be updated with the result of previous tasks
        param: action_name - the action to execute
        param: job_param - initial setting or result from the previous tasks
        returns: succes:bool, params:dict
        """
        try:
            new_action_param = json.loads(action_param % job_param)
        except KeyError as e:
            msg = u"action '%s' expects %s parameter" % (action_name, e)
            return False, {"error": msg}
        except ValueError as e:
            msg = u"action '%s' param can't be decoded from json %s \n %s" % (
                action_name,
                action_param,
                e
            )
            return False, {"error": msg}
        action = execute(action_name, new_action_param)
        execute(action_name, new_action_param)
        return not action.errors, action

    def on_task_error(self, on_error_action_param, on_error_action_name, repeated_param, job_param, task_to_repeat):
        """
        param: on_error_action_param
        param: on_error_action_name
        param: repeated_param
        param: job_param
        param: task_to_repeat
        """
        try:
            repeated_param_filled = json.loads(
                (repeated_param or '{}') % job_param
            )
        except KeyError as e:
            msg = "action '%s' expects %s parameters to repeated run" % (repeated_param, e)
            return False, {"error": msg}
        except:
            msg = """action '%s' can't parse json repeated parameters
            %s""" % repeated_param
            return False, {"error": msg}

        msg = "executing on error_action '%s' with param %s" % (
            on_error_action_name, repeated_param)
        self.log("info", msg)

        return getattr(self, on_error_action_name)(task_to_repeat, repeated_param_filled, on_error_action_param, job_param)

    def do_tasks(self, job_param, task_list):
        """
        Run tasks according to a recipe in specified order
        param: task_list
        param: job_param
        """

        for task_index, task in enumerate(task_list):
            action_param_or_default = task["action_param"] or '{}'
            success, task_result = self.do_task(
                task["action_name"], action_param_or_default, job_param)

            if not success:
                self.log("error", task_result.errors)
                return self.on_task_error(
                    task["on_error_action_param"], task["on_error_action_name"], 
                    task["repeated_param"], job_param, task["action_name"])

            # update job_param with result of task
            import ipdb; ipdb.set_trace()
            job_param.update(task_result.job_param)
            # output last task result and last success state
        return success, job_param

    def repeat_task(self, task_to_repeat, repeat_param, on_error_action_param, job_param):
        """
        max_attempts - required in job_param
        wait - optional in job_param, seconds
        """

        if "max_attempts" not in repeat_param:
            raise Exception("'max_attempts' must be set for repeat task")
        else:
            repeat_param["max_attempts"] = repeat_param["max_attempts"] - 1
        if repeat_param["max_attempts"] < 0:
            result = {};
            result["error"] = "Retrying the job wasn't successful"
            return False, result

        if "wait" in repeat_param:
            time.sleep(int(repeat_param["wait"]))

        result = task_to_repeat(on_error_action_param or '{}', job_param)
        success, state = result
        if success:
            return result
        else:
            return self.repeat_task(task_to_repeat, repeat_param, on_error_action_param, job_param)


    def finish(self, task_to_repeat, repeat_param, on_error_action_param, job_param):
        """
        Does nothing. Just finishes job
        """
        return False, job_param


