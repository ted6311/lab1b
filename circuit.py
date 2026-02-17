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



    def __assemble_system(self):

        # Build system_map
        nodes = set()
        for comp in self.components:
            nodes.update(comp.nodes)

        idx = 0
        for node in sorted(nodes):
            self.system_map[f"V{node}"] = idx
            idx += 1

        for comp in self.components:
            if not isinstance(comp, Ground):
                self.system_map[f"I_{comp.name}"] = idx
                idx += 1

        N = len(self.system_map)

        # Store as attributes (REQUIRED by spec)
        self.system_matrix = np.zeros((N, N), dtype=complex)
        self.system_rhs = np.zeros(N, dtype=complex)

        # Apply each component
        for comp in self.components:
            comp.apply(self.system_matrix,
                       self.system_rhs,
                       self.system_map,
                       self.frequency)

        # Apply KCL
        for node in sorted(nodes):
            if node == 0:
                continue

            row = self.system_map[f"V{node}"]

            for comp in self.components:
                if comp.nodes[0] == node:
                    self.system_matrix[row,
                    self.system_map[f"I_{comp.name}"]] += 1
                elif comp.nodes[1] == node:
                    self.system_matrix[row,
                    self.system_map[f"I_{comp.name}"]] -= 1
    def __solve(self):
        self.solution = np.linalg.solve(self.system_matrix, self.system_rhs)

    def run(self):
        self.__assemble_system()
        self.__solve()
        return self.solution


