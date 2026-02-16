from abc import ABC, abstractmethod
import numpy as np


class ElectricalComponent(ABC):
    def __init__(self, name: str, nodes: tuple, value: float):
        self.name = name
        self.nodes = nodes #(node1, node2)
        self.value = value
    @abstractmethod
    def apply(self, A, b, system_mAp, frequency):
        pass

    def apply_voltage(self, solution, system_mAp):
        n1, n2 = nodes
        