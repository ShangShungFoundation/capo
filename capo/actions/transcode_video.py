#!/usr/bin/python
import pexpect
#  http://stackoverflow.com/questions/7632589/getting-realtime-output-from-ffmpeg-to-be-used-in-progress-bar-pyqt4-stdout


def transcode_video(task_param):
    """
{"src": "inputfile.mov", "dst": "outputfile.mp4", "encoding": "-c:v libx264"}
{"src": "%(src)s", "dst": "%(dst)s", "encoding": "%(encoding)s"}
    """
    result = {}
    #import ipdb; ipdb.set_trace()
    try:
        cmd = 'avconv -i %(src)s %(encoding)s %(dst)s' % task_param
    except KeyError as e:
        msg = 'Transcode Video expects "%s" parameter'  % e
        result["error"] = msg
        return False, result
    try:
        thread = pexpect.spawn(cmd)
    except IOError as e:
        msg = 'Transcoding Error: %s' % e.strerror
        result["error"] = msg
        return False, result
    else:
        thread.expect(pexpect.EOF)
        status = thread.exitstatus
        result["job_param"] = {}
        if not status:
            result["error"] = thread.before.strip()
            return False, result
        else:
            result["job_param"]["transcoded"] = thread.before.strip()
            return True, result
