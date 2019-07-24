import sys
import random
from utils import Utils
from errors import Errors

import multiprocessing as mp
from functools import reduce

def createDictFromChoices(joineditems):
    dc = {}
    if not len(joineditems):
        return dc
    for value in joineditems.split(Utils.separator.value):
        if not len(value) or value in dc:
            continue
        dc[value] = 0
    return dc

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

class MyApp:
    DISPLAY_ON = False
    
    def __init__(self):
        pass

    def bestOutOfN(self, args):
        separator = ";"
        if len(args) < 3:
            Utils.displayHandler(Errors.not_enough_args.value, self.DISPLAY_ON)
            return Errors.not_enough_args.value
        elif not args[1].isdigit() or not int(args[1]) > 0:
            Utils.displayHandler(Errors.first_arg_not_int.value, self.DISPLAY_ON)
            return Errors.first_arg_not_int.value
        elif not separator in args[2]:
            Utils.displayHandler(Errors.missing_separator.value, self.DISPLAY_ON)
            return Errors.missing_separator.value
        n = int(args[1])
        choices = createDictFromChoices(args[2])
        if len(choices) <= 1:
            res = bestFromDict(choices)
        else:
            pool = mp.Pool(mp.cpu_count())
            results = [pool.apply(
                    incrementCountForChoice,
                    args=(choices, random.choice(choices.keys()))
                ) for __ in range(n)]
            pool.close()
            
            choices = reduce(countTally, results)
            
            res = bestFromDict(choices)
            Utils.displayHandler(
                ("\n"
                "BEST CHOICE:    {0}\n"
                "TOTAL SCORE:    {1}/{2}\n"
                "DISTRIBUTED:    {3}\n"
                ).format(res, str(choices[res]), n, str(choices)),
                self.DISPLAY_ON
            )

        return res

def incrementCountForChoice(choice_dict, key):
    choice_dict[key]+=1
    return choice_dict

def countTally(tally, current):
    for k in current:
        tally[k]+=current[k]
    return tally

if __name__ == "__main__":
    ma = MyApp()
    ma.DISPLAY_ON = True
    ma.bestOutOfN(sys.argv)