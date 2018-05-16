class SGW:
    def __init__(self):

        self.Shutter = {
            'MinValue': 0.0001,
            'MaxValue': 30,
            'Unit': 's',
            'Type': 'float'
        }

        self.GaindB = {
            'MinValue': 0,
            'MaxValue': 36,
            'Unit': 'dB',
            'Type': 'int'
        }

        self.WhiteBalance = {
            'MinValue': -2,
            'MaxValue': 6,
            'Unit': 'dB',
            'Type': 'int'
        }
