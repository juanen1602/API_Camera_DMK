import sys

sys.path.insert(0, 'JsonFile/Parameters/Brightness')
import brightness
from brightness import Brightness

sys.path.insert(0, 'JsonFile/Parameters/Gamma')
import gamma
from gamma import Gamma

sys.path.insert(0, 'JsonFile/Parameters/Gain')
import gain
from gain import Gain

sys.path.insert(0, 'JsonFile/Parameters/Exposure')
import exposure
from exposure import Exposure

sys.path.insert(0, 'JsonFile/Parameters/ExposureAuto')
import exposureauto
from exposureauto import ExposureAuto

class Parameters:        #Parameters
    def __init__(self):

        self.brightness = Brightness()

        self.gamma = Gamma()

        self.gain = Gain()

        self.exposure = Exposure()

        self.exposureauto = ExposureAuto()

        self.Parameters = {
            'Brightness': self.brightness.Brightness,
            'Gamma': self.gamma.Gamma,
            'Gain': self.gain.Gain,
            'Exposure': self.exposure.Exposure,
            'ExposureAuto': self.exposureauto.ExposureAuto
        }
