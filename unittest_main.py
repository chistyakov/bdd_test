import unittest
from collections import OrderedDict

from mock import patch

from main import CannotGetUserId, FullNameProviderRequestHandler, get_ordered_subdict



class TestGetUserId(unittest.TestCase):
    def setUp(self):
        #do not want to test the super class BaseRequestHandler
        #so constructor is patched
        self.patcher = patch('main.FullNameProviderRequestHandler.__init__', new=lambda x: None)
        self.patcher.start()
        #no need to pass anything to constructor
        self.handler = FullNameProviderRequestHandler()

    def test_with_port_slash_and_id(self):
        self.handler.path = "http://127.0.0.1:8080/?id=1"
        self.assertEqual(self.handler._get_user_id(), 1)

    def test_no_port_slash_and_id(self):
        self.handler.path = "http://127.0.0.1/?id=1"
        self.assertEqual(self.handler._get_user_id(), 1)

    def test_no_slash_and_id(self):
        self.handler.path = "http://127.0.0.1:8080?id=1"
        self.assertEqual(self.handler._get_user_id(), 1)

    def test_id_is_text1(self):
        self.handler.path = "http://127.0.0.1:8080?id==1"
        with self.assertRaises(CannotGetUserId):
            self.handler._get_user_id()

    def test_id_is_text2(self):
        self.handler.path = "http://127.0.0.1:8080?id=text"
        with self.assertRaises(CannotGetUserId):
            self.handler._get_user_id()

    def test_no_question_mark(self):
        self.handler.path = "http://127.0.0.1:8080id=1"
        with self.assertRaises(CannotGetUserId):
            self.handler._get_user_id()

    def test_no_id(self):
        self.handler.path = "http://127.0.0.1:8080?another=1"
        with self.assertRaises(CannotGetUserId):
            self.handler._get_user_id()

    def test_no_query(self):
        self.handler.path = "http://127.0.0.1:8080/user/1"
        with self.assertRaises(CannotGetUserId):
            self.handler._get_user_id()

    def test_two_id(self):
        self.handler.path = "http://127.0.0.1:8080/?id=1&id=2"
        self.assertEqual(self.handler._get_user_id(), 1)

    def test_two_params(self):
        self.handler.path = "http://127.0.0.1:8080/?id=1&hohoho=2"
        self.assertEqual(self.handler._get_user_id(), 1)

    def tearDown(self):
        self.patcher.stop()


class TestGetOrderedSubdict(unittest.TestCase):
    def test_simple_example(self):
        D = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.assertEqual(get_ordered_subdict(D, 'b', 'd'), OrderedDict([('b', 2), ('d', 4)]))

    def test_one_element_to_extract(self):
        D = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.assertEqual(get_ordered_subdict(D, 'b'), OrderedDict([('b', 2)]))

    def test_changed_order(self):
        D = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.assertEqual(get_ordered_subdict(D, 'd', 'a'), OrderedDict([('d', 4), ('a', 1)]))

    def test_key_not_exist(self):
        D = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.assertEqual(get_ordered_subdict(D, 'd', 'a', 'f'), OrderedDict([('d', 4), ('a', 1), ('f', '')]))
