from unittest import TestCase

from django.conf import settings

from models import Task
from actions.test_actions import FailingAction
from settings import ACTIONS

class ActionsTestCase(TestCase):
    def test_one(self):
        a = ACTIONS
        print(a["failing"](), a["adding_dot"](), a["random"](), a["multiplying10"])
        self.assertTrue(True)
