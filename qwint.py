import random
import qiskit
import matplotlib.pyplot as plt

qc = qiskit.QuantumCircuit(5,5)

a=0

qc.h([0,1,2,3,4])

qc.draw('mpl')
plt.show()

all_gates = [
    'H', 'X'
]

deck = [*(["H"]*10), *(["X"]*10)]
deck.remove("H")
gates = random.choices(deck, k=10)
deck.remove(gates)

hand_1 = []
gate = random.choice(all_gates)
hand_1.append(gate)
hand_1[0] = 'h'


qiskit.circuit.library.XGate
random.choices(gates, k=3)
figure = qc.draw("mpl")
figure.show()

