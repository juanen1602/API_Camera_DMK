class TemperatureHumidity:
    def __init__(self):

        self.TemperatureOperating = {
            'MinValue': -5,
            'MaxValue': 45,
            'Unit': 'ºC',
            'Type': 'int'
        }

        self.TemperatureStorage = {
            'MinValue': -20,
            'MaxValue': 60,
            'Unit': 'ºC',
            'Type': 'int'
        }

        self.HumidityOperating = {
            'MinValue': 20,
            'MaxValue': 80,
            'Unit': '%',
            'Type': 'int'
        }

        self.HumidityStorage = {
            'MinValue': 20,
            'MaxValue': 95,
            'Unit': '%',
            'Type': 'int'
        }
