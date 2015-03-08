import json
import time
import datetime

from models import Job, Log, FAILED, WAITING, RUNNING, COMPLETED
from worker import Worker


class Capo(object):
    """
    Singleton ruthlesly managing jobs.
    """
    jobs = []
    workers = []
    runs = {}  # stores runs to prevent infinite loop

    def get_awaiting_jobs(self):
        awaiting_jobs = Job.objects.filter(
            status__exact=WAITING,
            #execute_after__lte=datetime.datetime.now()
        ).order_by("submited_at")
        return awaiting_jobs

    def runing_jobs(self, recipe_id=None):
        qargs = dict(status__exact=RUNNING)
        if recipe_id:
            qargs["recipe_id"] = recipe_id
        runing_jobs = Job.objects.filter(**qargs).order_by("started_at")
        return runing_jobs

    def get_next_job(self):
        try:
            return self.get_awaiting_jobs()[0]
        except:
            return None

    def run_next_job(self):
        """runs job if all jobs of same kind are finished"""
        next_job = self.get_next_job()
        if not next_job:
            return None

        next_job_recipe = next_job.recipe
        max_jobs = next_job_recipe.max_jobs
        running_jobs = self.runing_jobs(next_job.recipe.id)

        if len(running_jobs) < max_jobs:
            return self.run_job(next_job.id)
        else:
            return None

    def repeat_job(self, job_id, job_param=None):
        run = Worker(job_id, job_param)
        return run

    def run_job(self, job_id, job_param=None, do_next_job=True):
        run = Worker()
        run.run_job(job_id, job_param)
        if job_id in self.runs:
            self.runs[job_id] = self.runs[job_id] + 1
        else:
            self.runs[job_id] = 1
        if run.current_job.status == FAILED and run.current_job.on_failure:
            if run.job.on_failure == "repeat":
                on_failure_param = json.loads(run.job.on_failure_param)
                max_repetitions = int(on_failure_param["max_repetitions"])
                if max_repetitions <= self.runs[job_id]:
                    self.run_job(job_id, False)

        self.jobs.append(run.current_job)
        if do_next_job:
            next_job = self.get_next_job()
            if next_job:
                self.run_job(next_job.id)

        return run
