#import sys

#sys.path.insert(0, 'JsonFile/Specifications/Adjustments/SGW')
import sgw
from sgw import SGW

class Adjustments:
    def __init__(self):

        self.sgw = SGW()

        self.Adjustments = {
            'Shutter': self.sgw.Shutter,
            'Gain': self.sgw.GaindB,
            'WhiteBalance': self.sgw.WhiteBalance
        }
