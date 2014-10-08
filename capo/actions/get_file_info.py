# -*- coding: utf-8 -*-
from repository.models import File


def get_file_info(task_param):
    """
    Gets file info
{"file_path": "xxx.xxx", "storage_id": "xxx.xxx"}
{"file_path": "%(path)s", "storage_id": %(storage_id)s}
    """
    result = {}
    try:
        file = File.objects.get(**task_param)
    except:
        msg = 'Cant find file: %(path)s in storage #%(storage_id)s' % task_param
        result["error"] = msg
        return False, result
    else:
        mount_point = file.storage.mount_point
        full_path = "/mnt/%s%s" % (mount_point.strip(), task_param["file_path"])
        result["job_param"] = file.__dict__
        result["job_param"]["file_type"] = file.mime.name
        result["job_param"]["mount_point"] = mount_point
        result["job_param"]["full_path"] = full_path
        result["job_param"]["ext"] = file.file_name.split(".")[1].lower()
        return True, result


def query_files(task_param):
    """
    Gets file info
{"path": "xxx.xxx", "storage_id": "xxx.xxx"}
{"path": "%(path)s", "storage_id": %(storage_id)s}
    """

    result = {}
    try:
        files = File.objects.filter(**task_param)
    except:
        msg = 'Error quering files'
        result["error"] = msg
        return False, result
    else:
        return True, files 
