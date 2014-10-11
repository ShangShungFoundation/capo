# -*- coding: utf-8 -*-

from cmd import cmd


class transfer_sh(cmd):
    """
    transfers file to https://transfer.sh/
{"file_path": "xxx.xxx"}
{"file_path": "%(file_path)s"}

result:
transfer_sh
    """
    expected_param = {"file_path": str}

    def run(self, action_param):
        file_path = action_param["file_path"]
        file_name = file_path.split(file_path)[-1]
        action_param = dict(
            cmd='curl --upload-file "%s" https://transfer.sh/%s' % (file_path, file_name)
        )
        return super(transfer_sh, self).run(action_param)
