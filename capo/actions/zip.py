#!/usr/bin/python
import pexpect
import logging


def zip_it(task_param):
    """
    zips file or directory
{"src": "xxx.xxx", "dst": "xxx.xxx"}
{"src": "%(src)s", "dst": "%(dst)s"}
    """
    result = {}
    cmd = 'zip -r %(dst)s %(src)s' % task_param

    try:
        thread = pexpect.spawn(cmd)
        logging.info('Files from %s zipped' % task_param["src"])
    except IOError as e:
        msg = 'Error zipping:  %s' % e.strerror
        result["error"] = msg
        return False, result
    else:
        return True, result
