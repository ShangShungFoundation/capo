class Action(object):
    """
    each action should have description

    """
    result = {}
    errors = []

    # to be defined in inherited class
    name = ""
    expected_param = {}
    optional_param = {}
    expected_result = {}
    

    def __init__(self, action_param):
        if action_param:
            self.action_param = action_param
            self.run(action_param)
    
    def run(self, action_param):
        # this should be overwritten 
        pass
    
    def error(self, msg):
        self.result["error"] = msg
        return False, self.result

    @classmethod
    def check_task_param(cls, action_param):
        errors = []
        for param in action_param:
            if param not in self.expected_param.keys():
                msg = "action '%s' requires '%s' parameter" % (cls.name, param)
                errors.append(msg)
        return errors




