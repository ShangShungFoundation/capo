from django.core.mail import send_mail
from django.conf import settings

from action import Action


class send(Action):
    """
    {"to": ["xxx.xxx"], "from": "xxx.xxx", "subject": "bbb", "message": "ggg"}
    {"to": ["%(to)s"], "from": "%(from)s", "subject": "%(subject)s", "message": "%(messsage)s"}
    """
    expected_param = {"to": list, "from": str, "subject": str, "message": unicode }

    def run(self, action_param):
        to = action_param["to"]
        sender = action_param["from"]
        subject = action_param["subject"]
        message = action_param.get("message")
        error_msg = "Can't send email with param %s" % action_param

        try:
            sent = send_mail(subject, message, sender, to, fail_silently=False)
        except:
            self.log_error(error_msg)
        else:
            if not sent:
                self.log_error(error_msg)
        return self.result()
