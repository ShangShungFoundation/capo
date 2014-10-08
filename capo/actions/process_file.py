# -*- coding: utf-8 -*-
import os


def process_file(task_param):
    """
    process file for delivery
    bitrate in Kb "-b:a 128k"
{"src": "xxx.xxx", "dst_dir": "xxx.xxx", "size": "xxx", "file_type": "xxx", "ext": "mmm"}
{"src": "%(src)s", "dst_dir": "%(dst)s", "size": %(size)s, "file_type": "%(file_type)s", "ext": "%(ext)s"}

returns:
files
    """

    result = {}
    src = task_param["src"]
    dst_dir = task_param["dst_dir"]
    size = task_param["size"]
    file_type = task_param["file_type"]
    ext = task_param["ext"]
    file_name = src.split("/")[-1]

    if file_type == "audio" and ext != "mp3":
        from conv_to_mp3 import conv_to_mp3
        result_file = os.path.join(dst_dir, "%s.mp3" % file_name)
        completed, conv_result = conv_to_mp3(dict(
            src=src,
            dst=result_file,
            bitrate="64k"
        ))
    elif file_type == "video" or ext == "mts":
        from transcode_video import transcode_video
        result_file = os.path.join(dst_dir, "%s.mp4" % file_name)
        completed, conv_result = transcode_video(dict(
            src=src,
            dst=result_file,
            encoding=""
        ))
    else:
        from cp import cp
        result_file = os.path.join(dst_dir, file_name)
        completed, conv_result = cp(dict(
            src=src,
            dst=result_file,
        ))
    result["files"] = [result_file]
    result["job_param"] = {}
    result.update(conv_result)
    result["job_param"]["result_file"] = result_file
    result["job_param"]["result_file_name"] = result_file.split("/")[-1]
    return completed, result
