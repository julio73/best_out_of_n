from enum import Enum

class Errors(Enum):
    not_enough_args = "not enough arguments"
    first_arg_not_int = "first argument must be a positive integer (>= 1)"
    missing_separator = "second argument must be a string of choices concatenated by the separator"
