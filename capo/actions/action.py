

class Action(object):
    """
    each action should have description

    """
    out = {}
    job_param = {}
    errors = []
    action_param = {}

    # to be defined in inherited class
    expected_param = {}  # {"src": [str, list], "dst_dir": str}
    optional_param = {}
    expected_result = {}
    
    def __init__(self, action_param = None):
        if action_param:
            self.action_param = action_param
            param_errors = self.valid_action_param(action_param)
            if param_errors:
                self.errors = param_errors

    def run(self, action_param):
        # this should be overwritten 
        pass

    def log_error(self, msg):
        self.errors.append(msg)
        return False

    def valid_action_param(self, action_param):
        errors = []
        for param in self.expected_param.keys():
            if param not in action_param:
                msg = "action '%s' requires '%s' parameter" % (self.__name__, param)
                errors.append(msg)
            
            param_value = action_param[param]
            expected_type = self.expected_param[param]

            if type(expected_type) == list:
                expected_types = expected_type
            else:
                expected_types = [expected_type]

            if type(param_value) not in expected_types:
                msg = "action '%s' %s=%s parameter should be %s instead %s" % (
                    self.__class__.__name__, 
                    param,
                    param_value,
                    expected_type,
                    type(param_value)
                )
                errors.append(msg)

        return errors if len(errors) > 0 else True


    @classmethod
    def valid_task_param(cls, action_param):
        errors = []
        for param in cls.expected_param.keys():
            if param not in action_param:
                msg = "task '%s' requires '%s' parameter" % (cls.__name__, param)
                errors.append(msg)

        return errors if len(errors) > 0 else True


