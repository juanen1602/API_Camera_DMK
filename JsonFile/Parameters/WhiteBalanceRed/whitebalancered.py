import sys

sys.path.insert(0, 'JsonFile/Parameters/Values')
import values
from values import Values

class WhiteBalanceRed:
    def __init__(self):

        self.values = Values(8, 0, 95, 32)

        self.Values = {
            'CurrentValue': self.values.CurrentValue,
            'MinValue': self.values.MinValue,
            'MaxValue': self.values.MaxValue,
            'DefaultValue': self.values.DefaultValue
        }

        self.WhiteBalanceRed = {
            'Value': self.Values,
            'Category': 'ByDefault',
            'Group': 'GrupoGain'
        }
