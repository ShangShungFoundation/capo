# -*- coding: utf-8 -*-
import pexpect
import logging


def conv_to_mp3(task_param):
    """
    Coverts usally WAV file to MP3
    bitrate in Kb "-b:a 128k"
{"src": "xxx.xxx", "dst": "xxx.xxx", "bitrate": "xxx"}
{"src": "%(dst)s", "dst": "%(dst)s", "bitrate": "%(bitrate)s"}
    """
    result = {}
    cmd = 'avconv -i "%(src)s" -b:a "%(bitrate)s" "%(dst)s"' % task_param
    try:
        thread = pexpect.spawn(cmd)
        logging.info('Transcoding video %(src)s to %(dst)s' % task_param)
    except IOError as e:
        msg = 'Coping Error: %s' % e.strerror
        result["error"] = msg
        return False, result
    else:
        return True, result

