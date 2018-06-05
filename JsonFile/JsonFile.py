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

#Response Codes

        self.CodeInformational = {
            'Code': None,
            'Info': None,
            'Parameters': None,
            'Example': None
        }

        self.CodeSuccess = {
            'Parameter': None,
            'Code': None,
            'Message': None,
            'Value': None
        }

        self.CodeSuccessResource = {
            'Code': None,
            'Message': None,
            'ID': None
        }

        self.CodeRedirection = {
            'Parameter': None,
            'Code': None,
            'Message': None,
            'MinValue': None,
            'MaxValue': None
        }

        self.CodeFailure = {
            'Parameter': None,
            'Code': None,
            'Message': None,
            'MinValue': None,
            'MaxValue': None
        }

        self.CodeFailureServer = {
            'Code': None,
            'Message': None
        }

