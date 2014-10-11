import shutil

from action import Action


class cp(Action):
    """
    This is similar to the Unix command cp -p.
    src - can be file path or list of file paths
{"src": "xxx.xxx", "dst_dir": "xxx.xxx"}
    """
    expected_param = {"src": [str, list], "dst_dir": str}
    optional_param = {"new_file_name": str}
    expected_result = {"job_param": {"result_files": list}}

    def cp(self, file_path, dst_dir, new_file_name=None):
        
        if new_file_name:
            file_name = new_file_name
        else:
            file_name = file_path.split("/")[-1]
        import ipdb; ipdb.set_trace()
        dst = "%s/%s" % (dst_dir, file_name)
        try:
            shutil.copy2(file_path, dst)
        # eg. src and dest are the same file
        except shutil.Error as e:
            msg = 'Coping Error: %s' % e
            self.log_error(msg)
        # eg. source or destination doesn't exist
        except IOError as e:
            msg = 'Coping Error: %s' % e.strerror
            self.log_error(msg)
        else:
            self.out["job_param"]["result_files"].append(file_name)
        
    def run(self, action_param):
        self.out["job_param"]["result_files"] = []
        src = action_param["src"]
        dst_dir = action_param["dst_dir"]
        new_file_name = action_param.get("new_file_name", None)
        if type(src) == str:
            self.cp(src, dst_dir, new_file_name)
        elif type(src) == list:
            for file_path in src:
                self.cp(src, dst_dir, new_file_name)
        return self.result()






