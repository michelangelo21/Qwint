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
        self.topframe = tk.Frame(self)
        self.topframe.grid(row=0, column=0, sticky='nsew')

        # for player 2 
        self.bottomframe = tk.Frame(self)
        self.bottomframe.grid(row=2, column=0, sticky='nsew')

        self.plotframe = tk.Frame(self)
        self.plotframe.grid(row=1, column=0, sticky='nsew')

        # for choosing wires
        self.control2_frame = tk.Frame(self)
        self.control2_frame.grid(row=1, column=1, sticky='nsew')

        self.control1_frame = tk.Frame(self)
        self.control1_frame.grid(row=1, column=2, sticky='nsew')


        self.target_frame = tk.Frame(self)
        self.target_frame.grid(row=1, column=3, sticky='nsew')

        self.control2_lbl = tk.Label(self.control2_frame, text='Control\nqubit')
        self.control2_wire = tk.IntVar()
        self.radio_control2 = [
            tk.Radiobutton(self.control2_frame, text="q"+str(i), variable=self.control2_wire, value=i, command=self.show_radio_control1)
            for i in range(num_wires)
        ]

        self.control1_lbl = tk.Label(self.control1_frame, text='Control\nqubit')
        self.control1_wire = tk.IntVar()
        self.radio_control1 = [
            tk.Radiobutton(self.control1_frame, text="q"+str(i), variable=self.control1_wire, value=i, command= lambda: self.show_radio_target(disable=[self.control1_wire.get()]))
            for i in range(num_wires)
        ]
        
        self.target_lbl = tk.Label(self.target_frame, text='Target\nqubit')
        self.target_wire = tk.IntVar()
        self.radio_target = [
            tk.Radiobutton(self.target_frame, text="q"+str(i), variable=self.target_wire, value=i, command=self.show_apply)
            for i in range(num_wires)
        ]


        self.rightframe = tk.Frame(self)
        self.rightframe.grid(row=1, column=4, sticky='nsew')

        all_gates = [
            'H', 'X', 'CX'
        ]

        self.qc = qiskit.QuantumCircuit(num_wires)
        self.initial_circuit()
        self.replot()

        self.round_no = 1
        self.active_player = 1
        self.p1_points = 0
        self.p2_points = 0

        self.p1_deck = [*(["H"]*12), *(["X"]*12),*(["CX"]*6)]
        self.p2_deck = self.p1_deck.copy()

        self.p1_hand = []
        self.draw(10, self.p1_deck, self.p1_hand)
        self.p2_hand = []
        self.draw(10, self.p2_deck, self.p2_hand)

        self.p1_pass = False
        self.p2_pass = False





        p1_hand = random.choices(all_gates, k=10)
        p1_hand.sort()
        p2_hand = random.choices(all_gates, k=10)
        p2_hand.sort()

        self.apply_button = tk.Button(
            self.rightframe,
            text="Apply",
            command=lambda: self.apply_gate(
                self.p1_hand[self.p1_choice.get()] if self.active_player == 1 else self.p2_hand[self.p2_choice.get()],
                [self.target_wire.get(), self.control1_wire.get(), self.control2_wire.get()]
            )
        )

        self.pass_button1 = tk.Button(
            self.rightframe,
            text="Pass",
            command=lambda: self.pass1()            
        )
        
        self.pass_button2 = tk.Button(
            self.rightframe,
            text="Pass",
            command=lambda: self.pass2()            
        )

        self.p1_choice = tk.IntVar()
        self.p2_choice = tk.IntVar()

        self.p1_radio = []
        self.p2_radio = []


        self.show_p1_choice()
        # self.show_p2_choice()


        tk.Button(self.rightframe, text='Quit', command=self.quit).pack()

    # end __init__

    def replot(self):
        try:
            self.fig_qc_canvas.get_tk_widget().destroy()
            self.fig_bloch_canvas.get_tk_widget().destroy()
        except:
            pass

        state = Statevector.from_instruction(self.qc)
        fig_bloch = plot_bloch_multivector_vertical(state)   

        fig_qc = self.qc.draw("mpl")

        fig_qc.set_size_inches(10, 6)
        fig_qc.tight_layout()

        fig_bloch.set_size_inches(2,6)
        fig_bloch.tight_layout()

        # create FigureCanvasTkAgg object
        self.fig_qc_canvas = FigureCanvasTkAgg(fig_qc, self.plotframe)
        self.fig_qc_canvas.get_tk_widget().pack(side=tk.LEFT, expand=0)

        self.fig_bloch_canvas = FigureCanvasTkAgg(fig_bloch, self.plotframe)
        self.fig_bloch_canvas.get_tk_widget().pack(side=tk.LEFT, expand=0)

    def draw(self, n_cards, deck, hand):
        if n_cards+len(hand)>10:
            n_cards = 10 - len(hand)
        for i in range (n_cards):
            gate = random.choice(deck)
            hand.append(gate)
            deck.remove(gate)
        hand.sort()

    def show_apply(self):
        self.apply_button.pack()

    def show_radio_control2(self):
        self.control2_lbl.pack(side=tk.TOP, fill=tk.X)
        for wire in self.radio_control2:
            wire.pack(side=tk.TOP, fill=tk.X, expand=1)

    def show_radio_control1(self):
        self.control1_lbl.pack(side=tk.TOP, fill=tk.X)
        for wire in self.radio_control1:
            wire.pack(side=tk.TOP, fill=tk.X, expand=1)

    def show_radio_target(self, disable=[]):
        if self.target_wire.get() in disable:
            self.apply_button.pack_forget()

        self.target_lbl.pack(side=tk.TOP, fill=tk.X)
        for i, wire in enumerate(self.radio_target):
            wire.pack(side=tk.TOP, fill=tk.X, expand=1)
            wire.configure(state=tk.NORMAL)
            if i in disable:
                wire.configure(state=tk.DISABLED)

    def show_wire_choices(self, gate):
        self.hide_wire_choices()

        if gate in ['H', 'X']:
            self.show_radio_target()
        elif gate in ['CX']:
            self.show_radio_control1()
        elif gate in ['CCX']:
            self.show_radio_control2()
        else:
            logging.ERROR("Gate not found")

    def hide_wire_choices(self):
        # self.apply_button.pack_forget()
        self.control1_lbl.pack_forget()
        self.control2_lbl.pack_forget()
        self.target_lbl.pack_forget()
        for wire in self.radio_control1:
            wire.pack_forget()
        for wire in self.radio_control2:
            wire.pack_forget()
        for wire in self.radio_target:
            wire.pack_forget()


    def show_p1_choice(self):
        self.p1_radio = [
            tk.Radiobutton(self.topframe, text=gate, variable=self.p1_choice, value=i, command= lambda: self.show_wire_choices(self.p1_hand[self.p1_choice.get()]))
            # tk.Radiobutton(self.topframe, text=gate, variable=self.p1_choice, value=i, command= lambda: self.show_wire_choices(self.p1_hand[self.p1_choice.get()])).pack(side=tk.LEFT, fill=tk.X, expand=1)
            for i, gate in enumerate(self.p1_hand)
        ]
        for r in self.p1_radio:
            r.pack(side=tk.LEFT, fill=tk.X, expand=1)


    def show_p2_choice(self):
        self.p2_radio = [
            tk.Radiobutton(self.bottomframe, text=gate, variable=self.p2_choice, value=i, command= lambda: self.show_wire_choices(self.p2_hand[self.p2_choice.get()]))
            for i, gate in enumerate(self.p2_hand)
        ]
        for r in self.p2_radio:
            r.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def hide_p1_choice(self):
        for r in self.p1_radio:
            r.destroy()
    
    def hide_p2_choice(self):
        for r in self.p2_radio:
            r.destroy()

    def initial_circuit(self):

        # self.qr = qiskit.QuantumRegister(6)
        # self.cr = qiskit.ClassicalRegister(6)
        # self.qc = qiskit.QuantumCircuit(self.qr, self.cr)
        self.qc = qiskit.QuantumCircuit(6)

    def board(self):
        self.hide_p1_choice()
        self.hide_p2_choice()
        if self.active_player == 1:
            self.show_p1_choice()
            if len(self.p1_hand) == 0:
                self.end_round()
        else:
            self.show_p2_choice()
        self.replot()

    def end_turn(self):
        
        if self.p1_pass == 1 or self.p2_pass == 1:
            self.board()
        elif self.p1_pass == 1 and self.p2_pass == 1:
            self.end_round()
            self.board()
        else:
            self.active_player = (self.active_player+1)%2
            self.board()

    def pass1(self):
        self.p1_pass = 1
        self.end_turn()

    def pass2(self):
        self.p2_pass = 1
        self.end_turn()

    def apply_gate(self, gate, wires):
        print(gate, wires)
        if gate == 'H': 
            self.qc.h(wires[0])
        elif gate == 'X': 
            self.qc.x(wires[0])
        elif gate == 'CX': 
            self.qc.cnot(wires[0], wires[1])
        
        self.end_turn()
        

    def win(self, wynik):
        print(wynik)

    def end_round(self):
        self.draw(5, self.p1_deck, self.p1_hand)
        self.draw(5, self.p2_deck, self.p2_hand)
        cr = qiskit.ClassicalRegister(6)
        self.qc.measure(range(6), cr)
        measure = 0
        for i in self.cr:
            measure =+ i
        if measure < 3:
            self.p1_points =+ 1
        elif measure > 3:
            self.p2_points =+ 1
        else:
            self.p1_points =+ 1
            self.p2_points =+ 1
        if self.p1_points == 2:
            if self.p2_points == 2:
                self.win('draw')
            else:
                self.win('player1 won')
        elif self.p2_points == 2:
            self.win('player2 won')
            

if __name__ == '__main__':
    app = App()
    app.mainloop()