from unittest import TestCase

from django.conf import settings

from models import Task, Recipe
from actions.test_actions import FailingAction
from settings import ACTIONS

class ActionsTestCase(TestCase):

    def assertNotRaises(self, fun):
        try:
            fun()
        except Exception as e:
            self.fail("Unexpected exception raised: %s " % e)

    def test_one_correctly_set_action_with_task_param(self):
        task = Task()
        task.action_name = "adding_dot"
        task.param = '{"parameter": "xxx"}'

        tasks = [task]

        self.assertNotRaises(lambda: Recipe.validate_tasks_inputs(tasks))

    def test_one_incorrectly_set_action_with_task_param(self):
        task = Task()
        task.action_name = "adding_dot"
        task.param = '{"parameter2": "xxx"}'
        tasks = [task]
        self.assertRaises(Exception, lambda: Recipe.validate_tasks_inputs(tasks))

    def test_correct_series_of_task_in_recipe(self):
        first_task = Task()
        first_task.action_name = "multiplying10"
        first_task.param = '{"number": 5}'

        second_task = Task()
        second_task.action_name = "adding_dot"
        second_task.order = 2
        second_task.param = '{"parameter": "%(number10)d"}'

        tasks = [first_task, second_task]
        self.assertNotRaises(lambda: Recipe.validate_tasks_inputs(tasks))
