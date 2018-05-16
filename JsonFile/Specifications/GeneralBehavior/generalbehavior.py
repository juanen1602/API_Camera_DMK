import sys

sys.path.insert(0, 'JsonFile/Specifications/GeneralBehavior/SDVVF')
import sdvvf
from sdvvf import SDVVF

class GeneralBehavior:
    def __init__(self):

        self.sdvvf = SDVVF()

        self.GeneralBehavior = {
            'Sensitivity': self.sdvvf.Sensitivity,
            'DynamicRange': self.sdvvf.DynamicRange,
            'VideoFormats': self.sdvvf.VideoFormats,
            'VideoFormatsPixels': self.sdvvf.VideoFormatsPixel,
            'FrameRateMaximum': self.sdvvf.FrameRateMaximum 
        }
