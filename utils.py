from enum import Enum

class Utils(Enum):
    separator = ";"

    @staticmethod
    def displayHandler(message, displayOn):
        if displayOn:
            print(message)