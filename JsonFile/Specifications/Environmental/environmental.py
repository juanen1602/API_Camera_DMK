import sys

sys.path.insert(0, 'JsonFile/Specifications/Environmental/TH')
import th
from th import TemperatureHumidity

class Environmental:
    def __init__(self):
   
        self.temperaturehumidity = TemperatureHumidity()

        self.Environmental = {
            'TemperatureOperating': self.temperaturehumidity.TemperatureOperating,
            'TemperatureStorage': self.temperaturehumidity.TemperatureStorage,
            'HumidityOperating': self.temperaturehumidity.HumidityOperating,
            'HumidityStorage': self.temperaturehumidity.HumidityStorage
        }
