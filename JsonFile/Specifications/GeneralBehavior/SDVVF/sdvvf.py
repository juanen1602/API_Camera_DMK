class SDVVF:
    def __init__(self):
        
        self.Sensitivity = {
            'Value': 0.05,
            'Unit': 'lux',
            'Type': 'float'
        }

        self.DynamicRange = {
            'Value': 8,
            'Unit': 'bit',
            'Type': 'int'
        }

        self.VideoFormats = {
            'Lenght': 1280,
            'Width': 960,
            'Unit': 'pixel',
            'Type': 'int'
        }

        self.VideoFormatsPixel = {
            'Total': 1.2*10**6,
            'Unit': 'pixel',
            'Type': 'int'
        }

        self.FrameRateMaximum = {
            'Value': 15,
            'Unit': 'fps',                #FramesperSecond
            'Type': 'int'
        }
