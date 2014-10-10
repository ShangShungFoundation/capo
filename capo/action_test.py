from unittest import TestCase

from django.conf import settings

from models import Task, Recipe
from actions.test_actions import FailingAction
from settings import ACTIONS

class ActionsTestCase(TestCase):
    def test_one_correctly_set_action_with_task_param(self):
        task = Task
        task.action_name = "adding_dot"
        task.param = '{"parameter": "xxx"}'

        tasks = [task]

        try:
            Recipe.validate_tasks_inputs(tasks)
        except Exception as e:
            self.fail("Unexpected exception raised: %s " % e)

    def test_one_incorrectly_set_action_with_task_param(self):
        task = Task
        task.action_name = "adding_dot"
        task.param = '{"parameter2": "xxx"}'
        tasks = [task]
        self.assertRaises(Exception, lambda: Recipe.validate_tasks_inputs(tasks))
