import random
import qiskit
import matplotlib.pyplot as plt

qc = qiskit.QuantumCircuit(5,5)

a=0

qc.h([0,1,2,3,4])

qc.draw('mpl')
plt.show()

gates = [
    'H', 'X'
]

qiskit.circuit.library.XGate
random.choices(gates, k=3)
figure = qc.draw("mpl")
figure.show()

