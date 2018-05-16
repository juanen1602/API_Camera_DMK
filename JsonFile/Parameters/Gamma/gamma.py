import sys

sys.path.insert(0, 'JsonFile/Parameters/Values')
import values
from values import Values

class Gamma:
    def __init__(self):

        self.values = Values(250, 1, 500, 16384)

        self.Values = {
            'CurrentValue': self.values.CurrentValue,
            'MinValue': self.values.MinValue,
            'MaxValue': self.values.MaxValue,
            'DefaultValue': self.values.DefaultValue
        }

        self.Gamma = {
            'Value': self.Values,
            'Category': 'ByDefault',
            'Group': 'GrupoGamma'
        }
