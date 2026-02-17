import numpy as np
from components import Ground

class Circuit:
    def __init__(self, frequency=0.0):
        self.frequency = frequency
        self.components = []
        self.system_map = {}
        self.system_matrix = None
        self. system_rhs = None
        self.solution = None
    def add_component(self, component):
        if component not in self.components:
            self.components.append(component)
        else:
            raise ValueError("Component {} already defined".format(component.name))




