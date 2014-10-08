# -*- coding: utf-8 -*-
import pexpect
import logging


def transfer_sh(task_param):
    """
    transfers file to https://transfer.sh/
{"src": "xxx.xxx", "file_name": "xxx.xxx"}
{"src": "%(dst)s", "file_name": "%(file_name)s"}

result:
transfer_sh
    """
    result = {}
    cmd = 'curl --upload-file "%(src)s" https://transfer.sh/%(file_name)s' % task_param
    try:
        thread = pexpect.spawn(cmd)
        logging.info('Transfering file "%(src)s" to transfer.sh' % task_param)
    except pexpect.TIMEOUT as e:
        msg = 'Curl command failed Error: %s' % e
        result["error"] = msg
        return False, result
    else:
        try:
            thread.expect(pexpect.EOF)
        except pexpect.TIMEOUT as e:
            msg = 'Curl command failed Error: %s' % e
            result["error"] = msg
            return False, result
        else:
            result["job_param"] = {}
            result["job_param"]["transfer_sh"] = thread.before.strip()
            return True, result
