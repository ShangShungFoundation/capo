from django.conf import settings

from actions.test_tasks import FailingTask

ACTIONS = dict(
    cp="capo.actions.cp",
    exe="capo.actions.exe",
    send="capo.actions.email",
    zip_it="capo.actions.zip",
    transcode_video="capo.actions.transcode_video",
    conv_to_mp3="capo.actions.exe",
    transfer_sh="capo.actions.transfer_sh",
)

CAPO_ACTIONS = getattr(settings, "CAPO_ACTIONS", {})

ACTIONS.update(CAPO_ACTIONS)

# where I set the Debug ???
settings.DEBUG = True

if settings.DEBUG:
    ACTIONS.update(dict(
        failing_task=FailingTask,
        adding_dot_task="capo.actions.test_tasks",
        randomly_task="capo.actions.test_tasks",
        multiplying10_task="capo.actions.multiplying10_task"
    ))
