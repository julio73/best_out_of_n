import sys
import random
from utils import Utils
from errors import Errors

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
            for __ in range(n):
                selected_key = random.choice(choices.keys())
                choices[selected_key]+=1
            res = bestFromDict(choices)
            Utils.displayHandler(
                ("\n"
                "BEST CHOICE:    {0}\n"
                "TOTAL COUNT:    {1}\n"
                "DISTRIBUTED:    {2}\n"
                ).format(res, str(choices[res]), str(choices)),
                self.DISPLAY_ON
            )

        return res



if __name__ == "__main__":
    ma = MyApp()
    ma.DISPLAY_ON = True
    ma.bestOutOfN(sys.argv)