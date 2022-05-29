import tkinter as tk
import logging
logging.basicConfig(level=logging.INFO)
import random
from turtle import left
import matplotlib
import qiskit

from qiskit.quantum_info import Statevector
# from qiskit.visualization import plot_bloch_multivector

from plot_bloch_multivector_vertical import plot_bloch_multivector_vertical

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Qwint')

        num_wires = 6

        # for player 1
        topframe = tk.Frame(self)
        # topframe.pack(side=tk.TOP, fill='both', expand=True)
        topframe.grid(row=0, column=0, sticky='nsew')

        midframe = tk.Frame(self)
        midframe.grid(row=1, column=0, sticky='nsew')

        # for player 2 
        bottomframe = tk.Frame(self)
        # bottomframe.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        bottomframe.grid(row=2, column=0, sticky='nsew')



        # for plot
        leftframe = tk.Frame(midframe)
        leftframe.pack(side='left')

        # for choosing wires
        rightframe = tk.Frame(midframe)
        rightframe.pack(side='right', fill='both', expand=True)

        all_gates = [
            'H', 'X'
        ]



        qc = qiskit.QuantumCircuit(num_wires,num_wires)
        qc.h(range(num_wires))
        qc.cnot(0,1)
        qc.h(2)
        qc.x(2)
        for i in range(10):
            qc.h(2)

        state = Statevector.from_instruction(qc)
        fig_bloch = plot_bloch_multivector_vertical(state)   

        fig_qc = qc.draw("mpl")

        fig_qc.set_size_inches(10, 6)
        fig_qc.tight_layout()

        fig_bloch.set_size_inches(2, 6)
        fig_bloch.tight_layout()

        # create FigureCanvasTkAgg object
        fig_qc_canvas = FigureCanvasTkAgg(fig_qc, leftframe)
        fig_qc_canvas.get_tk_widget().pack(side=tk.LEFT, expand=0)

        fig_bloch_canvas = FigureCanvasTkAgg(fig_bloch, leftframe)
        fig_bloch_canvas.get_tk_widget().pack(side=tk.LEFT, expand=0)

        wire_choice = tk.IntVar()
        for i in range(num_wires):
            tk.Radiobutton(leftframe, text="q"+str(i), variable=wire_choice, value=i).pack(side=tk.TOP, fill=tk.X, expand=1)

        p1_hand = random.choices(all_gates, k=10)
        p1_hand.sort()
        p2_hand = random.choices(all_gates, k=10)
        p2_hand.sort()

        self.p1_choice = tk.IntVar()
        self.p2_choice = tk.IntVar()

        for i in range(len(p1_hand)):
            tk.Radiobutton(topframe, text=p1_hand[i], variable=self.p1_choice, value=i, command= lambda: self.show_wire_choices(p1_hand[i])).pack(side=tk.LEFT, fill=tk.X, expand=1)

        for i in range(len(p2_hand)):
            tk.Radiobutton(bottomframe, text=p2_hand[i], variable=self.p2_choice, value=i).pack(side=tk.LEFT, fill=tk.X, expand=1)

        tk.Button(rightframe, text='Quit', command=self.quit).pack()

    def show_wire_choices(self, gate):
        pass

    def show_p1_choice(self):
        pass

if __name__ == '__main__':
    app = App()
    app.mainloop()