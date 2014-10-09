class Action(object):
    # to be defined in child class
    expected_param = {}
    optional_param = {}
    expected_result = {}
    
    result = {}
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
