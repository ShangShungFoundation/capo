from action import Action

class FailingAction(Action):

    expected_param = {}
    optional_param = {}
    expected_result = {}

    result = {}
    def run(self, action_param):
        """
            Task that always fails
        """
        result = "error"
        return True, result

class AddingDotAction(Action):
    def run(task_param):
        """ Task that adds '.' """
        parameter = task_param["parameter"] + "."
        result = {}
        result["job_param"] = {}
        result["job_param"]["parameter"] = parameter
        return True, result

class Multiplying10Action(Action):
    def run(task_param):
        """Task, that multiplies the number by 10"""
        multiply10 = task_param["number"] * 10
        result = {};
        result["job_param"] = dict(number10=multiply10)
        return True, result

class RandomAction(Action):
    def run(task_param):
        """ Task, that has 50% chance of success. """
        from random import random
        value = random()
        print("attempt", value, "bigger", task_param["threshold"])
        if value > task_param["threshold"]:
            res = True, dict(job_param=dict(value="Yes"))
        else:
            result = {}
            result["error"] = "failed"
            res = False, result
        return res
