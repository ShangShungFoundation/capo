from action import Action
from capo.worker import Job


class run_job(Action):
    """
{"job_id": job_id}
    """
    expected_param = {"job_id": [str, int]}
    
    def run(self, action_param):
        """
    {"job_id": xx}
        """
        job_id = task_param["job_id"]

        run = Job(job_id)
        # FIX
        return True, job_paramn_job