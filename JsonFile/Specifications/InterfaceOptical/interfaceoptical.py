import sys

sys.path.insert(0, 'JsonFile/Specifications/InterfaceOptical/Sensor')
import sensor
from sensor import CCDSensor

class InterfaceOptical:
    def __init__(self):

        self.ccdsensor = CCDSensor()

        self.InterfaceOptical = {
            'IRCutFilter': False,
            'SensorType': 'CCD',
            'SensorSpecification': 'SonyICX205AL',
            'Shutter': 'Global',
            'Format': self.ccdsensor.Format,
            'PixelSize': self.ccdsensor.PixelSize,
            'LensMount': 'C/CS'
        }
