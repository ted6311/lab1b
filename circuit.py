import numpy as np
from components import Ground

class Circuit:
    def __init__(self, frequency=0.0):
        # Skapar nödvändiga instans variabler
        self.frequency = frequency
        self.components = []
        self.system_map = {}
        self.system_matrix = None
        self.system_rhs = None
        self.solution = None

    # En metod för att lägga till komponenter i kretsen/systemet
    def add_component(self, component):
        # Om komponenten som ska läggas till inte redan finns i system så läggs den till
        if component not in self.components:
            self.components.append(component)
        else:
            # Om komponenten redan finns så visas ett fel, "error"
            raise ValueError("Component {} already defined".format(component.name))

    # En metod för att bygga systemet
    def __assemble_system(self):
        # Skapar ett set av unika noder
        nodes = set()
        # iterera genom komponenterna i kretsen och lägg till alla noderna
        for comp in self.components:
            nodes.update(comp.nodes)

        # En räknare för namngivandet av spänningarna och strömmarna i kretsen
        i = 0

        # Iterera genom alla unika noder
        for node in sorted(nodes):
            # Skapar en spänning i noden med identifierings index i
            self.system_map[f"V{node}"] = i
            i += 1

        # Itererar genom alla komponenter i kretsen
        for comp in self.components:
            # Om komponenten inte är en "Ground" så läggs en ström till
            if not isinstance(comp, Ground):
                # Lägger till en ström för komponenten med identifierings index i
                self.system_map[f"I_{comp.name}"] = i
                i += 1

        # Beräknar längden på vektorn system_map (unknowns), dvs x i Ax=b,
        # för att kunna skapa matris A och vektor b i rätt dimension respektive längd
        N = len(self.system_map)

        # Skapar system_matrix (A) och system_rhs (b), Ax=b
        self.system_matrix = np.zeros((N, N), dtype=complex)
        self.system_rhs = np.zeros(N, dtype=complex)

        # Iterera genom varje komponent i kretsen
        for comp in self.components:
            # Applicera varje komponent
            comp.apply(self.system_matrix, self.system_rhs, self.system_map, self.frequency)

        # Utför KCL för noderna i kretsen
        # Itererar genom alla noderna
        for node in sorted(nodes):
            # Ingen KCL för noder som är jordad ("grounded")
            if node == 0:
                continue

            # Sätter radnummer för nodens spänning i system_map (unknowns), dvs x i Ax=b
            # (Det vi hämtar är identifierings indexet i)
            row = self.system_map[f"V{node}"]

            # Ingoing or outgoing Resistor/Source
            # Iterera genom varje komponent i kretsen
            for comp in self.components:
                # Sätter +1 om iterationens nod är samma som komponentens "node 1", dvs före komponenten
                # Sätter -1 om iterationens nod är samma som komponentens "node 2" dvs efter komponenten
                if comp.nodes[0] == node:
                    self.system_matrix[row, self.system_map[f"I_{comp.name}"]] += 1
                elif comp.nodes[1] == node:
                    self.system_matrix[row, self.system_map[f"I_{comp.name}"]] -= 1

    # Metod för att lösa systemet
    def __solve(self):
        # Vi löser systemet, dvs beräknar x i Ax=b.
        self.solution = np.linalg.solve(self.system_matrix, self.system_rhs)

    # Metod för att köra systemet
    def run(self):
        # Bygger systemet
        self.__assemble_system()

        # Löser systemet
        self.__solve()

        # Returnerar lösningen
        return self.solution