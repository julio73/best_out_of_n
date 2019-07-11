import unittest
import sys
from enum import Enum
import random

class Utils(Enum):
    separator = ";"

class Errors(Enum):
    not_enough_args = "not enough arguments"
    first_arg_not_int = "first argument must be a positive integer (>= 1)"
    missing_separator = "second argument must be a string of choices concatenated by "+Utils.separator.value

def bestFromDict(dictionary):
    d = dictionary.copy()
    if len(d) == 0:
        return None
    best_so_far = d.popitem()
    while not len(d) == 0:
        next_item = d.popitem()
        if next_item[1] > best_so_far[1]:
            best_so_far = next_item
    return best_so_far[0]


def bestOutOfN(args):
    separator = ";"
    if len(args) < 3:
        print(Errors.not_enough_args.value)
        return Errors.not_enough_args.value
    elif not args[1].isdigit() or not int(args[1]) > 0:
        print(Errors.first_arg_not_int.value)
        return Errors.first_arg_not_int.value
    elif not separator in args[2]:
        print(Errors.missing_separator.value)
        return Errors.missing_separator.value
    n = int(args[1])
    choices = createDictFromChoices(args[2])
    if len(choices) <= 1:
        res = bestFromDict(choices)
    else:
        for trial in range(n):
            selected_key = random.choice(choices.keys())
            choices[selected_key]+=1
        res = bestFromDict(choices)
    print("\nBEST CHOICE:\t"+res+" \nTOTAL COUNT:\t"+str(choices[res])+"\nDISTRIBUTED:\t"+str(choices)+"\n")
    return res

def createDictFromChoices(joineditems):
    dc = {}
    if not len(joineditems):
        return dc
    for value in joineditems.split(Utils.separator.value):
        if not len(value) or value in dc:
            continue
        dc[value] = 0
    return dc

class TestBestOutOfN(unittest.TestCase):
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
        self.assertEqual(bestOutOfN([]), Errors.not_enough_args.value)
        self.assertEqual(bestOutOfN(["",""]), Errors.not_enough_args.value)

        self.assertNotEqual(bestOutOfN(["","",""]), Errors.not_enough_args.value)
    
    def test_arg1_isdigit(self):
        self.assertEqual(bestOutOfN(["","a",""]), Errors.first_arg_not_int.value)
        self.assertEqual(bestOutOfN(["","-100",""]), Errors.first_arg_not_int.value)
        self.assertEqual(bestOutOfN(["","0",""]), Errors.first_arg_not_int.value)

        self.assertEqual(bestOutOfN(["","1.34",""]), Errors.first_arg_not_int.value)

        self.assertNotEqual(bestOutOfN(["","10",""]), Errors.first_arg_not_int.value)
    
    def test_missing_separator(self):
        self.assertEqual(bestOutOfN(["","10",""]), Errors.missing_separator.value)

        self.assertNotEqual(bestOutOfN(["","10",""+Utils.separator.value]), Errors.missing_separator.value)
        self.assertNotEqual(bestOutOfN(["","10", str(Utils.separator.value).join(["foo","bar","buzz"])]), Errors.missing_separator.value)
    
    def test_best_out_of_n(self):
        res = bestOutOfN(["", "3", str(Utils.separator.value)])
        self.assertEqual(res, None)
        res = bestOutOfN(["", "1", "a"+Utils.separator.value+"b"])
        self.assertIn(res, ["a", "b"])
        res = bestOutOfN(["", "2", "a"+Utils.separator.value+"b"])
        self.assertIn(res, ["a", "b", "c"])
        res = bestOutOfN(["", "10", "a"+Utils.separator.value+"b"])
        self.assertIn(res, ["a", "b", "c"])

        res = bestOutOfN(["", "3", "a"+Utils.separator.value+"a"])
        self.assertNotIn(res, ["aa", "aaa", "`a`", ""])
        res = bestOutOfN(["", "5", "a"+Utils.separator.value+"d"])
        self.assertNotIn(res, ["aa", "b", "c"])

# unittest.main()

if __name__ == "__main__":
    bestOutOfN(sys.argv)