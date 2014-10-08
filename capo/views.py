import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from capo import Capo
from models import Job

capo = Capo()  # we initialize Capo solitary singleton


@login_required
def run_job(request):
    job_id = request.GET.get("job_id")
    run = capo.run_job(job_id)
    out = dict(
        job_id=job_id,
        job=run.job.recipe.name,
        completed=run.job.status,
        param=run.job_param,
    )
    return HttpResponse(
        json.dumps(out),
        content_type="application/json",
    )


@login_required
def submit_job(request, recipe_id):
    param = request.GET.copy()
    param_json = json.dumps(param.dict())
    job = Job.objects.create(
        recipe_id=recipe_id,
        param=param_json,
        submited_by=request.user,
    )
    out = dict(
        job_id=job.id
    )
    return HttpResponse(
        json.dumps(out),
        content_type="application/json",
    )


@login_required
def submit_job_and_run(request):
    param = request.GET.copy()
    param["user"] = request.user
    job = Job.objects.create(
        **param
    )

    run = capo.run_job(job.id)
    out = dict(
        job_id=job.id,
        job=run.job.process.name,
        completed=run.job.status,
        param=run.job_param,
    )
    return HttpResponse(
        json.dumps(out),
        content_type="application/json",
    )
