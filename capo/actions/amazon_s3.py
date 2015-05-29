import boto

from cmd import cmd
# http://stackoverflow.com/questions/10044151/how-to-generate-a-temporary-url-to-upload-file-to-amazon-s3-with-boto-library
from django.conf import settings


class amazon_upload(cmd):
    """

{"file_path": "xxx.xxx",
"file_path": "%(file_path)s"}
    """
    expected_param = {"file_path": str}

    def run(self, action_param):
        file_path = action_param["file_path"]

        c = boto.connect_s3()
        fp = open(file_path)
        content_length = len(fp.read())
        temp_url = c.generate_url(settings.seconds_available, 'PUT', settings.bucket_name, settings.s3_key)
        cmd = 'curl --request PUT --upload-file true_measure/test_files/test_file_w_content.txt "%s"' % temp_url
        return super(upload, self).run({"cmd": cmd})