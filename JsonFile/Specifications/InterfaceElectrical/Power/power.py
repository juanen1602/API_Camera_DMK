class SupplyPower:
    def __init__(self):

        self.SupplyVoltage = {
            'MinValue': 4.5,
            'MaxValue': 5.5,
            'Unit': 'Voltage',
            'Type': 'Float'
        }

        self.CurrentConsumption = {
            'Value': 500,
            'Unit': 'mA',
            'Type': 'int'
        }        
