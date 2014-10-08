#!/usr/bin/python
import pexpect
import logging
#  http://stackoverflow.com/questions/7632589/getting-realtime-output-from-ffmpeg-to-be-used-in-progress-bar-pyqt4-stdout


def exe(task_param):
    result = {}
    cmd = task_param["cmd"]

    try:
        thread = pexpect.spawn(cmd)
        logging.info('Executing command %s' % cmd)
    except:
        msg = 'Executing command "%s" Error: %s' % (cmd, e.strerror)
        result["error"] = msg
        return False, result
    else:
        return True, result
