
from cmd import cmd


class rm(cmd):
    """
{"path": "xxx.xxx"}
    """
    expected_param = {"path": [str, list]}
        
    def run(self, action_param):
        path = action_param["path"]
        if type(path) == list:
            cmd = cmd.join(", ")
        cmd = "rm -rf %s" % path
        return super(rm, self).run({"cmd": cmd})
