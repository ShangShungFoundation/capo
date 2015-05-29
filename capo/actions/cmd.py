import shlex
from subprocess import Popen, PIPE

from action import Action


class cmd(Action):
    """
{"cmd": cmd}
    """
    expected_param = {"cmd": [str, list]}

    def exe(self, cmd):
        """
        Execute the external command and get its exitcode, stdout and stderr.
        """
        args = shlex.split(cmd)

        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        #
        return exitcode, out, err

    def run(self, action_param):
        self.out["job_param"]["cmds"] = []
        cmd = action_param["cmd"]
        exitcode, out, err = self.exe(cmd)
        if not err:
            self.out["job_param"]["cmds"].append(out.strip())
        else:
            self.log_error(err)
        return self.result()
