import os
from unittest import TestCase

from django.conf import settings

from models import Task, Recipe
#from actions.test_actions import FailingAction
from settings import ACTIONS

from actions.cp import cp
from actions.email import send
from actions.cmd import cmd
from actions.transfer_sh import transfer_sh
from actions.rm import rm
from actions.zip_it import zip_it


CUR_DIR = os.path.dirname(os.path.dirname(__file__))
TEST_DIR = os.path.join(CUR_DIR, "capo", "test")


class TestCp(TestCase):
    def setUp(self):
        self.test_dir = os.path.join(CUR_DIR, "capo", "test")

    def test_cp_wrong_param(self):

        c = cp({"src": "dddd/sds.tiff", "dst_dir": "fffff"})
        success, result = c.result()
        self.assertFalse(success)
        self.assertEqual(result["errors"][0], 'Coping Error: No such file or directory')


    def test_cp_1_file(self):
        src = os.path.join(self.test_dir, "img.jpg")
        dst_dir = os.path.join(self.test_dir, "dir")
        #import ipdb; ipdb.set_trace()
        c = cp({"src": src, "dst_dir": dst_dir})
        success, result = c.result()
        
        self.assertEqual(success, True)
        self.assertEqual(result["job_param"]["result_files"][0], 'img.jpg')



class TestTaskValidation(TestCase):
    def setUp(self):
        self.test_dir = os.path.join(CUR_DIR, "capo", "test")

    def test_valid_task_param(self):
        c = cp()
        valid = c.valid_task_param({"src": "dddd/sds.tiff", "dst_dir": "fffff"})
        self.assertTrue(valid)
        

    def test_valid_task_param_missing(self):
        c = cp()
        valid = c.valid_task_param({"src": "dddd/sds.tiff"})
        #self.assertEqual(valid[0], "action 'cp' requires 'dst_dir' parameter")


class TestActionValidation(TestCase):
    def setUp(self):
        self.test_dir = os.path.join(CUR_DIR, "capo", "test")

    def test_valid_action_param(self):
        src = os.path.join(self.test_dir, "img.jpg")
        dst_dir = os.path.join(self.test_dir, "dir")
        c = cp()
        valid = c.valid_action_param({"src": src, "dst_dir": dst_dir})
        self.assertTrue(valid)
        

    def test_valid_action_param_wrong_type(self):
        src = os.path.join(self.test_dir, "img.jpg")
        dst_dir = os.path.join(self.test_dir, "dir")
        c = cp()
        valid = c.valid_action_param({"src": 3, "dst_dir": dst_dir})
        self.assertEqual(valid[0], "action 'cp' src=3 parameter should be [<type 'str'>, <type 'list'>] instead <type 'int'>")


class TestEmail(TestCase):
    def test_wrong_param(self):

        pass


class TestCmd(TestCase):
    def test_cmd(self):
        c = cmd({"cmd":"ls"})
        success, result = c.result()
        self.assertTrue(success)
        self.assertEqual(result["job_param"]["cmds"][0], "capo_test\ndb.sqlite3\nmanage.py")


class TestTransferSh(TestCase):
    def test_transferg_sh(self):
        file_path = os.path.join(TEST_DIR, "img.jpg")
        #import ipdb; ipdb.set_trace()
        t = transfer_sh({"file_path":file_path})
        success, result = t.result()
        self.assertTrue(success)


class TestZip(TestCase):
    def test_zip_file(self):
        src = os.path.join(TEST_DIR, "img.jpg")
        dst = "img.zip"
        
        z = zip_it({"src": src, "dst":dst})
        success, result = z.result()
        self.assertTrue(success)

        
        