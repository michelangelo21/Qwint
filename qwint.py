import random
import qiskit
import matplotlib.pyplot as plt

qc = qiskit.QuantumCircuit(5,5)

a=0
n_cards1 = 7    # number of cards in 1st player hand
n_cards2 = 10   # number of cards in 2nd player hand
n_h = 12     # number of gates h in deck
n_x = 12 
n_cx = 6
deck_size = n_h+n_x+n_cx


qc.h([0,1,2,3,4])

qc.draw('mpl')
plt.show()

gates = [
    'H', 'X', 'CX'
]

deck_1 = []

def deck_build(deck, n, card):
    for j in range(n):
        deck.append(card)


deck_build(deck_1, n_h,  'H' )
deck_build(deck_1, n_x,  'X' )
deck_build(deck_1, n_cx, 'CX')

deck_2 = deck_1

hand_1 = []
hand_2 = []

def draw(n_cards, deck, hand):
    for i in range (n_cards):
        n_gate = random.randint(0, len(deck)-1)
        hand.append(deck[n_gate])
        del deck[n_gate]

draw(n_cards1, deck_1, hand_1)
draw(n_cards2, deck_2, hand_2)



qiskit.circuit.library.XGate
random.choices(gates, k=3)
figure = qc.draw("mpl")
figure.show()

