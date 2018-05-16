import size
from size import Size

class InterfaceMechanical:
    def __init__(self):

        self.size = Size()

        self.InterfaceMechanical = {
            'Dimension': self.size.Dimension,
            'Mass': self.size.Mass 
        }
