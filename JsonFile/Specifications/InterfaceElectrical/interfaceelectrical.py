import sys

sys.path.insert(0, 'JsonFile/Specifications/InterfaceElectrical/Power')
import power
from power import SupplyPower

class InterfaceElectrical:
    def __init__(self):

        self.supplypower = SupplyPower()

        self.InterfaceElectrical = {
            'Interface': 'USB2.0-USB-3.0',
            'SupplyVoltage': self.supplypower.SupplyVoltage,
            'CurrentConsumption': self.supplypower.CurrentConsumption,
            'AutoIrisControl': False,
            'Trigger': False,
            'IOs': False
        }
