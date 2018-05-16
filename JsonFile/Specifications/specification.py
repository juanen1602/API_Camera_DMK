import sys

sys.path.insert(0, 'JsonFile/Specifications/GeneralBehavior')
import generalbehavior
from generalbehavior import GeneralBehavior

sys.path.insert(0, 'JsonFile/Specifications/InterfaceOptical')
import interfaceoptical
from interfaceoptical import InterfaceOptical

sys.path.insert(0, 'JsonFile/Specifications/InterfaceElectrical')
import interfaceelectrical
from interfaceelectrical import InterfaceElectrical

sys.path.insert(0, 'JsonFile/Specifications/InterfaceMechanical')
import interfacemechanical
from interfacemechanical import InterfaceMechanical

sys.path.insert(0, 'JsonFile/Specifications/Adjustments')
import adjustments
from adjustments import Adjustments

sys.path.insert(0, 'JsonFile/Specifications/Environmental')
import environmental
from environmental import Environmental

class Specifications:
    def __init__(self):

        self.generalbehavior = GeneralBehavior()

        self.interfaceoptical = InterfaceOptical()

        self.interfaceelectrical = InterfaceElectrical()

        self.interfacemechanical = InterfaceMechanical()

        self.adjustments = Adjustments()

        self.environmental = Environmental()

        self.Specification = {
            'GeneralBehavior': self.generalbehavior.GeneralBehavior,
            'Interface(Optical)': self.interfaceoptical.InterfaceOptical,
            'Interface(Electrical)': self.interfaceelectrical.InterfaceElectrical,
            'Interface(Mechanical)': self.interfacemechanical.InterfaceMechanical,
            'Adjustments': self.adjustments.Adjustments,
            'Environmental': self.environmental.Environmental
        }
