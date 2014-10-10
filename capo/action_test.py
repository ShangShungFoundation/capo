from unittest import TestCase

from django.conf import settings

from models import Task, Recipe
from actions.test_actions import FailingAction
from settings import ACTIONS

class ActionsTestCase(TestCase):
    def test_one_correctly_set_action_with_task_param(self):
        a = ACTIONS

        task = Task
        task.action_name = a["adding_dot"]
        task.param = '{"parameter": "xxx"}'

        tasks = [task]

        result = Recipe.validate_tasks_inputs(tasks)

        self.assertTrue(result)
