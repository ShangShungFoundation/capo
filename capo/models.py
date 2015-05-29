from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from settings import ACTIONS
from json import dumps


def load_action(actions, action_name):
<<<<<<< HEAD
    return getattr(
        __import__(actions[action_name],
        fromlist=[action_name]), action_name
    )

=======
    #
    return getattr(__import__(actions[action_name], fromlist=[action_name]), action_name)
>>>>>>> 62d7909b87249234de027d288dfae03420544162

def describe_actions(actions):
    desc = {}
    for action_name in actions:
        action = load_action(actions, action_name)
        desc[action_name] = {}
        desc[action_name]['expected_param'] = getattr(action, "expected_param", "")
        desc[action_name]['desc'] = action.__doc__

    return desc


def json_serial(obj):
    if isinstance(obj, type):
        "return total number of minutes"
        return str(obj)


class Recipe(models.Model):
    """
    Defines tasks and initial parameters for a job
    """
    name = models.CharField(max_length=255)
    label = models.SlugField()
    max_jobs = models.SmallIntegerField("max parallel jobs", default=1)
    param = models.TextField(blank=True, null=True,
        help_text="template for formating parametrs values so they can be \
        rterived form 'job_param'")
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def action_desc(cls):
        Job
        return dumps(describe_actions(ACTIONS), default=json_serial)


COMMUNICATION = (
    ("db", "db"),
)


class Worker(models.Model):
    """
    Defines worker which can be specialized in some recepies
    """
    name = models.CharField(
        max_length=150)

    #accepts = models.ManyToManyField(
    #    Recipe, blank=True)

    location = models.CharField(
        max_length=250,
        default="localhost",
        help_text="url to communicate with the worker",)
    communication = models.CharField(max_length=30, choices=COMMUNICATION)
    active = models.BooleanField()

    def __unicode__(self):
        return self.name


class WorkerCapacity(models.Model):
    worker = models.ForeignKey(User)
    capacity = models.ForeignKey(Recipe)
    max_jobs = models.SmallIntegerField("max parallel jobs", default=1)


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

    def clear(self):
        action = load_action(ACTIONS, self.action_name)
        valid_task_param = action.valid_task_param(self.param)
        if not valid_task_param:
            raise ValidationError(valid_task_param.join("\n"))


CODES = ["info", "warning", "error"]

FAILED = 0
WAITING = 1
RUNNING = 2
COMPLETED = 3

STATUS = (
    (FAILED, "failed"),
    (WAITING, "waiting"),
    (RUNNING, "running"),
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
