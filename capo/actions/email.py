from django.core.mail import send_mail
from django.conf import settings


def send(task_param):
    """
{"to": ["xxx.xxx"], "from": "xxx.xxx", "subject": "bbb", "message": "ggg"}
{"to": ["%(to)s"], "from": "%(from)s", "subject": "%(subject)s", "message": "%(messsage)s"}
    """
    result = {}
    to = task_param["to"]
    sender = task_param["from"]
    subject = task_param["subject"]
    message = task_param.get("message")

    try:
        sent = send_mail(subject, message, sender, to, fail_silently=False)
    except:
        msg = "Can't send email %s" % task_param
        result["error"] = msg
        return False, result
    else:
        if sent:
            return True, result
        else:
            result["error"] = "email not sent"
            return False, result


def send_admin(job_param, task_param):
    """
{"to": ["xxx.xxx"], "from": "xxx.xxx", "subject": "bbb", "message": "ggg"}
{"to": ["%(to)s"], "from": "%(from)s", "subject": "%(subject)s", "message": "%(messsage)s"}
    """
    to = settings.ADMINS
    sender = task_param["from"]
    subject = task_param["subject"]
    messsage = task_param.get("message")

    try:
        send_mail(subject, messsage, sender, to, fail_silently=False)
    except:
        msg = "Can't send email to %s" % to
        job_param["error"] = msg
        return False, job_param
    else:
        return True, job_param
