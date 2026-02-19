from abc import ABC, abstractmethod
import numpy as np


class ElectricalComponent(ABC):
    def __init__(self, name: str, nodes: tuple, value: float):
        self.name = name
        self.nodes = nodes #(node1, node2)
        self.value = value

    # @abstractmethod gör så att alla subklasser är tvugna att implementera och skriva sin egen version
    @abstractmethod
    def apply(self, A, b, system_mAp, frequency):
        pass

    def get_voltage(self, solution, system_mAp):
        n1, n2 = self.nodes
        v1 = solution[system_mAp[f"V{n1}"]]
        v2 = solution[system_mAp[f"V{n2}"]]
        return v1 - v2
    @abstractmethod
    def get_current(self, solution, system_mAp):
        pass



class Resistor(ElectricalComponent):
    def apply(self, A, b, system_mAp, frequency):
        v1 = system_mAp[f"V{self.nodes[0]}"]
        v2 = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        #Resistance
        R = self.value

        # Ohm law
        A[i, v1] = 1
        A[i, v2] = -1
        A[i, i] = -R

    def get_current(self, solution, system_mAp):
        i = system_mAp[f"I_{self.name}"]
        return solution[i]

class VoltageSource(ElectricalComponent):
    def apply(self, A, b, system_mAp, frequency):
        v_p = system_mAp[f"V{self.nodes[0]}"]
        v_m = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        # V_plus - V_minus = voltage in voltage source
        A[i, v_p] = 1
        A[i, v_m] = -1
        b[i] = self.value

    def get_current(self, solution, system_mAp):
        return solution[system_mAp[f"I_{self.name}"]]

class Inductor(ElectricalComponent):
    def apply(self, A, b, system_mAp, frequency):

        w = 2*np.pi*frequency   # w = 2*pi*f omega
        Z = 1j*w*self.value # Z_L=jwL, Impedance
        v1 = system_mAp[f"V{self.nodes[0]}"]
        v2 = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        # Ohm
        A[i,v1] = 1
        A[i,v2] = -1
        A[i,i] = -Z
    def get_current(self, solution, system_mAp):
        return solution[system_mAp[f"I_{self.name}"]]

class Capacitor(ElectricalComponent):
    def apply(self, A, b, system_mAp, frequency):
        w = 2*np.pi*frequency   # w = 2*pi*f
        Z = 1/(1j*w*self.value) # Z_C = 1/(jwC), impedance
        v1 = system_mAp[f"V{self.nodes[0]}"]
        v2 = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        # OHMS
        A[i,v1] = 1
        A[i,v2] = -1
        A[i,i] = -Z
    def get_current(self, solution, system_mAp):
        return solution[system_mAp[f"I_{self.name}"]]

class Ground(ElectricalComponent):
    def __init__(self, node):
        super().__init__("GND", (node, node), 0)
    def apply(self, A, b, system_mAp, frequency):
        v = system_mAp[f"V{self.nodes[0]}"]
        A[v,v] = 1
        b[v] = 0
    def get_current(self, solution, system_mAp):
        return 0