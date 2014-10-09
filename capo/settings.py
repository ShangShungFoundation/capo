from django.conf import settings

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
