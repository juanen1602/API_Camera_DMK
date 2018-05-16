import sys

sys.path.insert(0, 'JsonFile/Parameters')
import parameters
from parameters import Parameters

sys.path.insert(0, 'JsonFile/Specifications')
import specification
from specification import Specifications

class JSONFile:
    def __init__(self):

        self.parameters = Parameters()

        self.specifications = Specifications()

        self.File = {
            'Widget': None,
            'SingleSerial': None,
            'ConnectionType': None,
            'Specification': self.specifications.Specification,
            'Parameters': self.parameters.Parameters
        }
