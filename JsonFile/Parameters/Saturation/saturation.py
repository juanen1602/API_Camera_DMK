import sys

sys.path.insert(0, 'JsonFile/Parameters/Values')
import values
from values import Values

class Saturation:
    def __init__(self):

        self.values = Values(10, 0, 256, -8193)

        self.Values = {
            'CurrentValue': self.values.CurrentValue,
            'MinValue': self.values.MinValue,
            'MaxValue': self.values.MaxValue,
            'DefaultValue': self.values.DefaultValue
        }

        self.Saturation = {
            'Value': self.Values,
            'Category': 'ByDefault',
            'Group': 'GrupoSaturation'
        }
