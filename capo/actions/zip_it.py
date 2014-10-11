# -*- coding: utf-8 -*-

from cmd import cmd


class zip_it(cmd):
    """
    zips file or directory
{"src": "xxx.xxx", "dst": "xxx.xxx"}
{"src": "%(src)s", "dst": "%(dst)s"}
    """
    expected_param = {"src": [str, list], "dst": str}, 

    def run(self, action_param):
        src = action_param["src"]
        dst = action_param["dst"]
        if type(src) == list:
            src = src.join(" ")
        cmd = 'zip %s %s' % (dst, src)
        return super(zip_it, self).run({"cmd":cmd })
