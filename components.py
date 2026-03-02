from abc import ABC, abstractmethod
import numpy as np

class ElectricalComponent(ABC):
    def __init__(self, name: str, nodes: tuple, value: float):
        # Skapar nödvändiga instans variabler
        self.name = name
        self.nodes = nodes # (node1, node2)
        self.value = value

    # @abstractmethod gör så att alla subklasser är tvungna att implementera och skriva sin egen version
    @abstractmethod
    def apply(self, A, b, system_mAp, frequency):
        # Applicerar komponenten olika, beroende på komponent typen
        # Se de olika komponent klasserna nedan.
        pass

    # En metod för att hämta spänning över en viss komponent i kretsen
    def get_voltage(self, solution, system_mAp):
        # Identifierar noderna som komponenten är kopplad mellan
        n1, n2 = self.nodes

        # Hämtar spänningarna för noderna
        v1 = solution[system_mAp[f"V{n1}"]]
        v2 = solution[system_mAp[f"V{n2}"]]

        # Returnerar skillnaden, vilket är spänningen över komponenten
        return v1 - v2

    @abstractmethod
    def get_current(self, solution, system_mAp):
        # Hämtar strömmen, vilket görs olika beroende på komponent typ.
        # Se de olika komponent klasserna nedan.
        pass

# Komponent av typ "Resistor"
class Resistor(ElectricalComponent):
    # Resistorns apply metod
    def apply(self, A, b, system_mAp, frequency):
        # Hämtar identifierings indexet för spänningarna i de två kopplade noderna samt strömmen
        v1 = system_mAp[f"V{self.nodes[0]}"]
        v2 = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        # Sätter resistorns värde
        R = self.value

        # Ohms lag i system_matrix, dvs A i Ax=b
        A[i, v1] = 1/R
        A[i, v2] = -1/R
        A[i, i] = -1

    # Resistorns get_current metod
    def get_current(self, solution, system_mAp):
        # Hämtar raden för spänningen
        i = system_mAp[f"I_{self.name}"]

        # Returnerar lösningen på spänningen för den hämtade raden
        return solution[i]

# Komponent av typ "VoltageSource"
class VoltageSource(ElectricalComponent):
    # VoltageSource apply metod
    def apply(self, A, b, system_mAp, frequency):
        # Hämtar identifierings indexet för spänningarna i de två kopplade noderna samt strömmen
        v_p = system_mAp[f"V{self.nodes[0]}"]
        v_m = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        # V_plus - V_minus = spänning i spänningskällan
        A[i, v_p] = 1
        A[i, v_m] = -1
        b[i] = self.value

    # VoltageSource get_current metod
    def get_current(self, solution, system_mAp):
        return solution[system_mAp[f"I_{self.name}"]]

# Komponent av typ "Inductor"
class Inductor(ElectricalComponent):
    # Induktorns apply metod
    def apply(self, A, b, system_mAp, frequency):
        # Beräknar vinkelfrekvensen, omega
        w = 2*np.pi*frequency   # w = 2*pi*f omega

        # Beräknar impedansen
        Z = 1j*w*self.value # Z_L=jwL, Impedance

        # Hämtar identifierings indexet för spänningarna i de två kopplade noderna samt strömmen
        v1 = system_mAp[f"V{self.nodes[0]}"]
        v2 = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        # Ohms lag
        A[i,v1] = 1/Z
        A[i,v2] = -1/Z
        A[i,i] = -1

    # Induktorns get_current metod
    def get_current(self, solution, system_mAp):
        return solution[system_mAp[f"I_{self.name}"]]

# Komponent av typ "Capacitor"
class Capacitor(ElectricalComponent):
    # Kondensatorns apply metod
    def apply(self, A, b, system_mAp, frequency):
        # Beräknar vinkelfrekvensen, omega
        w = 2*np.pi*frequency   # w = 2*pi*f

        # Beräknar impedansen
        Z = 1/(1j*w*self.value) # Z_C = 1/(jwC), impedance

        # Hämtar identifierings indexet för spänningarna i de två kopplade noderna samt strömmen
        v1 = system_mAp[f"V{self.nodes[0]}"]
        v2 = system_mAp[f"V{self.nodes[1]}"]
        i = system_mAp[f"I_{self.name}"]

        # Ohms lag
        A[i,v1] = 1/Z
        A[i,v2] = -1/Z
        A[i,i] = -1

    # Kondensatorns get_current metod
    def get_current(self, solution, system_mAp):
        return solution[system_mAp[f"I_{self.name}"]]

# Komponent av typ "Ground"
class Ground(ElectricalComponent):
    def __init__(self, node):
        # Hämtar attribut från Electrialcomponents
        super().__init__("GND", (node, node), 0)

    # Jordens apply metod
    def apply(self, A, b, system_mAp, frequency):
        v = system_mAp[f"V{self.nodes[0]}"]
        A[v,v] = 1
        b[v] = 0

    # Jordens get_current metod
    def get_current(self, solution, system_mAp):
        return 0