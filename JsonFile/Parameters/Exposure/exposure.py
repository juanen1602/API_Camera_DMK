import sys

sys.path.insert(0, 'JsonFile/Parameters/Values')
import values
from values import Values

class Exposure:
    def __init__(self):

        self.values = Values(50, 0, 100, 8192)

        self.Values = {
            'CurrentValue': self.values.CurrentValue,
            'MinValue': self.values.MinValue,
            'MaxValue': self.values.MaxValue,
            'DefaultValue': self.values.DefaultValue
        }

        self.Exposure = {
            'Value': self.Values,
            'Category': 'ByDefault',
            'Group': 'GrupoBrightness'
        }
