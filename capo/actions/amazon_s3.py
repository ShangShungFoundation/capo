import os
import datetime

import boto
from boto.s3.key import Key

from action import Action
from django.conf import settings


class amazon_upload(Action):
    """
    {"file_path": "xxx.xxx",
    "file_path": "%(file_path)s"}
    """
    expected_param = {"file_path": str}
    
    def run(self, action_param):
        file_path = action_param["file_path"]
        file_name = file_path.split("/")[-1]
        aws_dir = action_param.get("aws_dir", datetime.datetime.now().isoformat())

        c = boto.connect_s3(
            settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        b = c.get_bucket(settings.AWS_BUCKET_NAME)
        k = Key(b)
        k.key = "%s/%s" % (aws_dir, file_name)
        k.set_contents_from_filename(file_path)
        temp_url = k.generate_url(settings.AWS_SECONDS_AWAILABLE, 'GET')
        self.job_param["temp_url"] = temp_url