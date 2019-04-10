import sys

sys.path.insert(0, 'JsonFile/Parameters/Values')
import values
from values import Values

class Hue:
    def __init__(self):

        self.values = Values(200, 0, 359, -8193)

        self.Values = {
            'CurrentValue': self.values.CurrentValue,
            'MinValue': self.values.MinValue,
            'MaxValue': self.values.MaxValue,
            'DefaultValue': self.values.DefaultValue
        }

        self.Hue = {
            'Value': self.Values,
            'Category': 'ByDefault',
            'Group': 'GrupoGain'
        }
