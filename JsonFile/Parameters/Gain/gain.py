import sys

sys.path.insert(0, 'JsonFile/Parameters/Values')
import values
from values import Values

class Gain:
    def __init__(self):

        self.values = Values(500, 260, 1023, 32768)

        self.Values = {
            'CurrentValue': self.values.CurrentValue,
            'MinValue': self.values.MinValue,
            'MaxValue': self.values.MaxValue,
            'DefaultValue': self.values.DefaultValue
        }

        self.Gain = {
            'Value': self.Values,
            'Category': 'ByDefault',
            'Group': 'GrupoGain'
        }
