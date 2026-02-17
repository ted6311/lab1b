import numpy as np
import matplotlib.pyplot as plt
from components import *
from circuit import Circuit


# 4.1 Resistive DC
def part_41():

    c = Circuit()

    V1 = VoltageSource("V1", (1, 0), 1)
    V2 = VoltageSource("V2", (2, 3), 2)
    R1 = Resistor("R1", (1, 2), 2000)
    R2 = Resistor("R2", (3, 0), 3000)
    R3 = Resistor("R3", (3, 0), 1000)
    G  = Ground(0)

    c.add_component(V1)
    c.add_component(V2)
    c.add_component(R1)
    c.add_component(R2)
    c.add_component(R3)
    c.add_component(G)

    sol = c.run()

    # Calculate required values
    i0 = R2.get_current(sol, c.system_map)
    i1 = R1.get_current(sol, c.system_map)
    v0 = R3.get_voltage(sol, c.system_map)
    print("\n--- 4.1 Results ---")
    print("i0 =", i0, "A")
    print("i1 =", i1, "A")
    print("v0 =", v0, "V")
    print(" \n 4.1 component values")
    for name, idx in c.system_map.items():
        print(name, "=", sol[idx])


# 4.2 Sweep

def part_42():

    temps = np.linspace(0, 100, 100)
    voltages = []

    for T in temps:

        R3_value = 100 + 100*T*0.00385

        c = Circuit()

        c.add_component(VoltageSource("V1", (1, 0), 1))
        c.add_component(Resistor("R1", (1, 2), 100))
        c.add_component(Resistor("R2", (2, 0), 10))
        c.add_component(Resistor("R4", (3, 0), 10))
        c.add_component(Resistor("R3", (2, 3), R3_value))
        c.add_component(Ground(0))

        sol = c.run()

        v0 = sol[c.system_map["V3"]]
        voltages.append(np.real(v0))

    plt.plot(temps, voltages)
    plt.xlabel("Temperature (°C)")
    plt.ylabel("v0 (V)")
    plt.title("PT100 Voltage vs Temperature")
    plt.show()


# 4.3 AC Sweep

def part_43():

    freqs = np.logspace(2, 7, 500)
    gain = []
    phase = []

    for f in freqs:

        c = Circuit(frequency=f)

        c.add_component(VoltageSource("VAC", (1, 0), 1))
        c.add_component(Resistor("R1", (1, 2), 2200))
        c.add_component(Resistor("R2", (2, 0), 500))
        c.add_component(Inductor("L1", (1, 2), 1e-3))
        c.add_component(Capacitor("C1", (2, 0), 100e-9))
        c.add_component(Ground(0))

        sol = c.run()

        vout = sol[c.system_map["V2"]]

        gain.append(abs(vout))
        phase.append(np.angle(vout, deg=True))

    plt.subplot(2, 1, 1)
    plt.semilogx(freqs, gain)
    plt.ylabel("Gain")

    plt.subplot(2, 1, 2)
    plt.semilogx(freqs, phase)
    plt.ylabel("Phase (deg)")
    plt.xlabel("Frequency (Hz)")

    plt.show()


if __name__ == "__main__":
    part_41()
    part_42()
    part_43()