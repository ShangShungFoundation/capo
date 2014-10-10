from unittest import TestCase

from django.conf import settings

from models import Task
from actions.test_tasks import FailingTask
from settings import ACTIONS

class ActionsTestCase(TestCase):
    def test_one(self):
        ft = ACTIONS["failing_task"]()
        print ft.result
        self.assertTrue(True)
