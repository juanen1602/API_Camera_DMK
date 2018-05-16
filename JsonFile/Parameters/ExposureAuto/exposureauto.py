import sys

sys.path.insert(0, 'JsonFile/Parameters/Values')
import values
from values import Values

class ExposureAuto:
    def __init__(self):

        self.values = Values(50, None, None, 8192)

        self.Values = {
            'CurrentValue': self.values.CurrentValue,
            'DefaultValue': self.values.DefaultValue
        }

        self.ExposureAuto = {
            'Value': self.Values,
            'Category': 'ByDefault',
            'Group': 'GrupoBrightness'
        }
