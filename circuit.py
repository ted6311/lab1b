import numpy as np
from components import Ground

class Circuit:
    def __init__(self, frequency=0):
        self.frequency = frequency
        self.components = []
        self.system_map = {}
        self.solution = None
