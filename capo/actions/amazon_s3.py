import boto
import os

from django.conf import settings
# http://stackoverflow.com/questions/10044151/how-to-generate-a-temporary-url-to-upload-file-to-amazon-s3-with-boto-library


def upload(task_param):
    """
    This is similar to the Unix command cp -p.

{"file_path": "xxx.xxx",
"file_path": "%(file_path)s"}
    """
    file_path = task_param["file_path"]

    c = boto.connect_s3()
    fp = open(file_path)
    content_length = len(fp.read())
    temp_url = c.generate_url(settings.seconds_available, 'PUT', settings.bucket_name, settings.s3_key)
    os.system('curl --request PUT --upload-file true_measure/test_files/test_file_w_content.txt "'+temp_url+'"')
    return True, result