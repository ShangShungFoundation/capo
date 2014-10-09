import shutil
import logging


def cp(task_param):
    """
    This is similar to the Unix command cp -p.

{"src": "xxx.xxx",
"dst": "xxx.xxx"}
    """
    result = {}
    src = task_param["src"]
    dst = task_param["dst"]
    try:
        logging.info('Coping %s to %s' % (src, dst))
        shutil.copy2(src, dst)
    # eg. src and dest are the same file
    except shutil.Error as e:
        msg = 'Coping Error: %s' % e
        result["error"] = msg
        return False, task_param
    # eg. source or destination doesn't exist
    except IOError as e:
        msg = 'Coping Error: %s' % e.strerror
        result["error"] = msg
        return False, result
    else:
        return True, result
