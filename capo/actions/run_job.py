from capo.capo import RunJob

def run_job(job_param, task_param):
    """
{"job_id": xx}
    """
    job_id = task_param["job_id"]

    run = RunJob(job_id)
    return True, job_param