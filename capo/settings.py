from django.conf import settings

from actions.test_actions import FailingAction, AddingDotAction, RandomAction, Multiplying10Action

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
        failing=FailingAction,
        adding_dot=AddingDotAction,
        random=RandomAction,
        multiplying10=Multiplying10Action,
    ))
