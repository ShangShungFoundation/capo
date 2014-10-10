import json
import time
import datetime

from models import Job, Log, FAILED, WAITING, RUN, COMPLETED

from settings import ACTIONS

def execute(action_name, action_param):
    action = getattr(__import__(ACTIONS[action_name]), action_name)
    return action(action_param)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.timedelta):
        "return total number of minutes"
        return "%.2f" % obj.total_seconds() / 60

    if isinstance(obj, datetime.datetime):
        return str(obj)


class RunJob(object):
    """docstring for RunJob"""
    job = None
    job_param = {}
    original_task_list = []
    status = RUN

    def __init__(self, job_id, job_param=None):
        job = Job.objects.get(pk=job_id)
        self.job = job
        self.job_param = json.loads(job.param)
        if job_param:
            self.job_param.update(job_param)
        if job.status in [WAITING, FAILED]:
            job.status = self.status
            job.started_at = datetime.datetime.now()
            job.save()
            self.job_param['job_id'] = job.id
            self.job = job
            job_tasks = job.recipe.task_set.all().order_by("order")
            for job_task in job_tasks:
                self.original_task_list.append(dict(
                    action_name=job_task.action_name,
                    action_param=job_task.param,
                    on_error_action_name=job_task.on_error_action,
                    on_error_action_param=job_task.on_error_param,
                    repeated_param=job_task.repeated_run_param,
                ))
            task_list = self.original_task_list
            completed, job_param = self.do_tasks(task_list, self.job_param)
            if completed:
                self.job.status = 3
                self.job.completed_at = datetime.datetime.now()
                self.result = json.dumps(job_param, default=json_serial)
            else:
                self.job.status = 0
            self.job.save()

    def do_task(self, action_name, action_param, job_param):
        """
            Run the task
            action_param - the param that can be updated with the result of previous tasks
            action_name - the action to execute
            job_param - initial setting or result from the previous tasks
        """
        # we update action_param with latest job_parameters
        try:
            new_action_param = json.loads(
                action_param % job_param
            )
        except KeyError as e:
            msg = "action '%s' expects %s parameter" % (action_name, e)
            return False, {"error": msg}
        except ValueError as e:
            msg = "action '%s' param can't be decoded from json %s \n %s" % (
                action_name,
                action_param,
                e
            )
            return False, {"error": msg}
        return execute(action_name, new_action_param)

    def on_task_error(self, on_error_action_param, on_error_action_name, repeated_param, job_param, task_to_repeat):

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
            on_error_action_name, repeated_param
        )

        logged = Log.objects.create(**dict(
            job_id=self.job.id,
            msg=msg,
            code="info"
        ))

        return getattr(self, on_error_action_name)(task_to_repeat, repeated_param_filled, on_error_action_param, job_param)

    def do_tasks(self, task_list, job_param):
        """
            Run tasks according to a recipe in specified order
        """

        for task_index, task in enumerate(task_list):

            def do_task_with_params(action_param, job_param):
                return self.do_task(task["action_name"], action_param, job_param)

            action_param_or_default = task["action_param"] or '{}'
            res = do_task_with_params(action_param_or_default, job_param)

            success, task_result = res
            if not success:
                logged = Log.objects.create(**dict(
                    job_id=self.job.id,
                    msg=task_result["error"],
                    code="error"
                ))

                on_task_error_success, on_task_error_result = self.on_task_error(
                    task["on_error_action_param"], task["on_error_action_name"], 
                    task["repeated_param"], job_param, do_task_with_params
                )
                break
            # update job_param with result of task
            if "job_param" in task_result:
                job_param.update(task_result["job_param"])
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


