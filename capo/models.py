from django.db import models
from django.contrib.auth.models import User

from settings import ACTIONS
from json import loads

class Recipe(models.Model):
    """
    Defines tasks and initial parameters for a job
    """
    name = models.CharField(max_length=255)
    label = models.SlugField()
    max_jobs = models.SmallIntegerField(default=1)
    param = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    @staticmethod
    def validate_tasks_inputs(tasks, job):
        job_param = loads(job.param)
        for task in tasks:
            task_action = ACTIONS[task.action_name]()
            # check if the applying runs correctly, the types do match
            try:
                params_applied = task.param % job_param
                loaded_dict = loads(params_applied)
                job_param.update(loaded_dict)
            except Exception as e:
                raise Exception("wrong job params")
            # check if the task has all expected params
            for expected_param in task_action.expected_params:
                if not expected_param in job_param:
                    raise Exception("recipe not configured correctly")
            # update the job_param for the next run
            job_param.update(task_action.expected_result)

class Worker(models.Model):
    """
    Defines worker which can be spetialized in some recepies
    """
    name = models.CharField(
        blank=True, null=True,
        max_length=150)
    accepts = models.ManyToManyField(Recipe,
        blank=True, null=True)

    def __unicode__(self):
        return self.id

ON_ERROR = ["finish", "repeat_task"]


class Task(models.Model):
    """
    Defines action, its parameters and failback action
    """
    recipe = models.ForeignKey(Recipe)
    order = models.SmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    action_name = models.CharField(
        max_length=20,
        choices=zip(ACTIONS.keys(), ACTIONS.keys())
    )
    param = models.TextField(blank=True, null=True)

    on_error_action = models.CharField(
        max_length=50, choices=zip(ON_ERROR, ON_ERROR))
    on_error_param = models.TextField(blank=True, null=True)
    repeated_run_param = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.action_name

    class Meta:
        ordering = ('order', )

CODES = ["info", "warning", "error"]

FAILED = 0
WAITING = 1
RUN = 2
COMPLETED = 3

STATUS = (
    (FAILED, "failed"),
    (WAITING, "waiting"),
    (RUN, "running"),
    (COMPLETED, "completed"),
)

ON_FAILURE = (
    ("repeat", "repeat"),
)


class Job(models.Model):
    """
    Defines job parameters for Recipe execution,
    status of execution, and failback bahaviour.
    Job parameters overwrite Recipe parameters.
    """
    recipe = models.ForeignKey(Recipe)
    worker = models.ForeignKey(Worker, blank=True, null=True)
    param = models.TextField()
    #priority = models.SmallIntegerField(default=1)

    status = models.SmallIntegerField(choices=STATUS,  default=1)
    execute_after = models.DateTimeField(
        null=True, blank=True)

    submited_at = models.DateTimeField(auto_now_add=True)
    submited_by = models.ForeignKey(User)

    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    result = models.TextField(
        null=True, blank=True)

    on_failure = models.CharField(
        choices=ON_FAILURE,
        blank=True, null=True,
        max_length=50)
    on_failure_param = models.TextField(
        null=True, blank=True,
        help_text="""if 'repeat' is selected for job failure
        action 'max_attempts' must be set as parameter""")

    observations = models.TextField(
        null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.recipe, self.status)


class Log(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job)
    msg = models.TextField()
    code = models.CharField(max_length=16, choices=zip(CODES, CODES))

    def __unicode__(self):
        return u"%s %s job: #%s %s" % (
            self.time, self.code.upper(), self.job.id, self.msg
        )

    class Meta:
        ordering = ('-time', )
