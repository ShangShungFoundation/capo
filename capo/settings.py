from django.conf import settings

ACTIONS = dict(
    cp="capo.actions.cp",
    rm="capo.actions.rm",
    cmd="capo.actions.cmd",
    send="capo.actions.email",
    zip_it="capo.actions.zip_it",
    run_job="capo.actions.run_job",
    transfer_sh="capo.actions.transfer_sh",
    amazon_upload="capo.actions.amazon_s3",
)

CAPO_ACTIONS = getattr(settings, "CAPO_ACTIONS", {})

ACTIONS.update(CAPO_ACTIONS)

if settings.DEBUG:
    ACTIONS.update(dict(
        # failing=FailingAction,
        # adding_dot=AddingDotAction,
        # random=RandomAction,
        # multiplying10=Multiplying10Action,
    ))
