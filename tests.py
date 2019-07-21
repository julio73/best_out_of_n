import sys
import unittest

from main import *
from utils import Utils
from errors import Errors 

class TestBestOutOfN(unittest.TestCase):
    my_boon_app = None

    def setUp(self):
        self.my_boon_app = MyApp()

    def test_create_dict_from_choices(self):
        res = createDictFromChoices(str(Utils.separator.value).join(["",""]))
        self.assertEqual(res, {})
        res = createDictFromChoices(str(Utils.separator.value).join(["","a"]))
        self.assertEqual(res, {"a": 0})
        res = createDictFromChoices(str(Utils.separator.value).join(["a","","a", "aa", "c"]))
        self.assertEqual(res, {"a": 0, "aa": 0, "c": 0})
        res = createDictFromChoices(str(Utils.separator.value).join(["a","b","c"]))
        self.assertEqual(res, {"a": 0, "b": 0, "c": 0})
        res = createDictFromChoices(str(Utils.separator.value).join(["a","a","c"]))
        self.assertEqual(res, {"a": 0, "c": 0})

    def test_best_from_dict(self):
        d = {}
        self.assertEqual(bestFromDict(d), None)
        d = {"a": 1, "b": 3, "c": 2}
        self.assertEqual(bestFromDict(d), "b")
        d = {"a": 1, "b": 1, "c": 2}
        self.assertEqual(bestFromDict(d), "c")
        d = {"a": 1, "b": 1, "c": 1}
        self.assertEqual(bestFromDict(d), "a")
        d = {"a": 10000000, "b": 100, "c": 100000000}
        self.assertEqual(bestFromDict(d), "c")
        d = {"a": -30000000, "b": 20, "c": -100000000, "d": 123}
        self.assertEqual(bestFromDict(d), "d")
        
    def test_min_arg(self):
        self.assertEqual(self.my_boon_app.bestOutOfN([]), Errors.not_enough_args.value)
        self.assertEqual(self.my_boon_app.bestOutOfN(["",""]), Errors.not_enough_args.value)

        self.assertNotEqual(self.my_boon_app.bestOutOfN(["","",""]), Errors.not_enough_args.value)
    
    def test_arg1_isdigit(self):
        self.assertEqual(self.my_boon_app.bestOutOfN(["","a",""]), Errors.first_arg_not_int.value)
        self.assertEqual(self.my_boon_app.bestOutOfN(["","-100",""]), Errors.first_arg_not_int.value)
        self.assertEqual(self.my_boon_app.bestOutOfN(["","0",""]), Errors.first_arg_not_int.value)

        self.assertEqual(self.my_boon_app.bestOutOfN(["","1.34",""]), Errors.first_arg_not_int.value)

        self.assertNotEqual(self.my_boon_app.bestOutOfN(["","10",""]), Errors.first_arg_not_int.value)
    
    def test_missing_separator(self):
        self.assertEqual(self.my_boon_app.bestOutOfN(["","10",""]), Errors.missing_separator.value)

        self.assertNotEqual(self.my_boon_app.bestOutOfN(["","10",""+Utils.separator.value]), Errors.missing_separator.value)
        self.assertNotEqual(self.my_boon_app.bestOutOfN(["","10", str(Utils.separator.value).join(["foo","bar","buzz"])]), Errors.missing_separator.value)
    
    def test_best_out_of_n(self):
        res = self.my_boon_app.bestOutOfN(["", "3", str(Utils.separator.value)])
        self.assertEqual(res, None)
        res = self.my_boon_app.bestOutOfN(["", "1", "a"+Utils.separator.value+"b"])
        self.assertIn(res, ["a", "b"])
        res = self.my_boon_app.bestOutOfN(["", "2", "a"+Utils.separator.value+"b"])
        self.assertIn(res, ["a", "b", "c"])
        res = self.my_boon_app.bestOutOfN(["", "10", "a"+Utils.separator.value+"b"])
        self.assertIn(res, ["a", "b", "c"])

        res = self.my_boon_app.bestOutOfN(["", "3", "a"+Utils.separator.value+"a"])
        self.assertNotIn(res, ["aa", "aaa", "`a`", ""])
        res = self.my_boon_app.bestOutOfN(["", "5", "a"+Utils.separator.value+"d"])
        self.assertNotIn(res, ["aa", "b", "c"])

if __name__ == "__main__":
    unittest.main()
