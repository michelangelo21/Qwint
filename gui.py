import tkinter as tk
import logging

logging.basicConfig(level=logging.INFO)
import random
from turtle import left
import matplotlib
import qiskit
from qiskit import Aer

from qiskit.quantum_info import Statevector

# from qiskit.visualization import plot_bloch_multivector

from plot_bloch_multivector_vertical import plot_bloch_multivector_vertical

matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

NUM_WIRES = 6


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Qwint")

        # for player 1
        self.topframe = tk.Frame(self)
        self.topframe.grid(row=0, column=0, sticky="nsew")

        # for player 2
        self.bottomframe = tk.Frame(self)
        self.bottomframe.grid(row=2, column=0, sticky="nsew")

        self.plotframe = tk.Frame(self)
        self.plotframe.grid(row=1, column=0, sticky="nsew")

        # for choosing wires
        self.control2_frame = tk.Frame(self)
        self.control2_frame.grid(row=1, column=1, sticky="nsew")

        self.control1_frame = tk.Frame(self)
        self.control1_frame.grid(row=1, column=2, sticky="nsew")

        self.target_frame = tk.Frame(self)
        self.target_frame.grid(row=1, column=3, sticky="nsew")

        self.control2_lbl = tk.Label(self.control2_frame, text="^\nControl\nqubit")
        self.control2_wire = tk.IntVar()
        self.radio_control2 = [
            tk.Radiobutton(
                self.control2_frame,
                text="q" + str(i),
                variable=self.control2_wire,
                value=i,
                command=self.show_radio_control1,
            )
            for i in range(NUM_WIRES)
        ]

        self.control1_lbl = tk.Label(self.control1_frame, text="^\nControl\nqubit")
        self.control1_wire = tk.IntVar()
        self.radio_control1 = [
            tk.Radiobutton(
                self.control1_frame,
                text="q" + str(i),
                variable=self.control1_wire,
                value=i,
                command=lambda: self.show_radio_target(
                    disable=[self.control1_wire.get()]
                ),
            )
            for i in range(NUM_WIRES)
        ]

        self.target_lbl = tk.Label(self.target_frame, text="^\nTarget\nqubit")
        self.target_wire = tk.IntVar()
        self.radio_target = [
            tk.Radiobutton(
                self.target_frame,
                text="q" + str(i),
                variable=self.target_wire,
                value=i,
                command=self.show_apply,
            )
            for i in range(NUM_WIRES)
        ]

        self.rightframe = tk.Frame(self)
        self.rightframe.grid(row=1, column=4, sticky="nsew")

        self.qc = qiskit.QuantumCircuit(NUM_WIRES, NUM_WIRES)
        self.initial_circuit()
        self.replot()

        self.round_no = 1
        self.active_player = 1
        self.p1_points = 0
        self.p2_points = 0

        self.p1_deck = [
            *(["H"] * 12),
            *(["X"] * 12),
            *(["Y"] * 6),
            *(["Z"] * 6),
            *(["S"] * 6),
            *(["T"] * 6),
            *(["CX"] * 8),
            *(["CCX"] * 2),
        ]
        self.p2_deck = self.p1_deck.copy()

        self.p1_hand = []
        self.draw(6, self.p1_deck, self.p1_hand)
        self.p2_hand = []
        self.draw(6, self.p2_deck, self.p2_hand)

        self.p1_pass = False
        self.p2_pass = False

        # p1_hand = random.choices(all_gates, k=10)
        # p1_hand.sort()
        # p2_hand = random.choices(all_gates, k=10)
        # p2_hand.sort()

        self.apply_button = tk.Button(
            self.rightframe,
            text="Apply",
            command=lambda: self.apply_gate(
                self.p1_hand[self.p1_choice.get()]
                if self.active_player == 1
                else self.p2_hand[self.p2_choice.get()],
                [
                    self.target_wire.get(),
                    self.control1_wire.get(),
                    self.control2_wire.get(),
                ],
            ),
        )

        self.lbl_p1 = tk.Label(self.topframe, text="Player 1's hand: ")
        self.pass_button1 = tk.Button(
            self.topframe, text="Pass", command=lambda: self.pass_round()
        )

        self.lbl_p2 = tk.Label(self.bottomframe, text="Player 2's hand: ")
        self.pass_button2 = tk.Button(
            self.bottomframe, text="Pass", command=lambda: self.pass_round()
        )

        self.p1_choice = tk.IntVar()
        self.p2_choice = tk.IntVar()

        self.p1_radio = []
        self.p2_radio = []

        self.show_p1_choice()
        # self.show_p2_choice()

        tk.Button(self.rightframe, text="Quit", command=self.quit).pack()
        self.lbl_score = tk.Label(
            self.rightframe,
            text=f"Score\n Player1: {self.p1_points}\n Player2: {self.p2_points}\n Round no {self.round_no}",
        )
        self.lbl_score.pack()

    # end __init__

    def replot(self):
        try:
            self.fig_qc_canvas.figure.clear()
            self.fig_bloch_canvas.figure.clear()
            self.fig_qc_canvas.get_tk_widget().destroy()
            self.fig_bloch_canvas.get_tk_widget().destroy()
        except:
            pass

        state = Statevector.from_instruction(self.qc)
        fig_bloch = plot_bloch_multivector_vertical(state)

        fig_qc = self.qc.draw("mpl")

        fig_qc.set_size_inches(10, 6)
        fig_qc.tight_layout()

        fig_bloch.set_size_inches(2, 6)
        fig_bloch.tight_layout()

        # create FigureCanvasTkAgg object
        self.fig_qc_canvas = FigureCanvasTkAgg(fig_qc, self.plotframe)
        self.fig_qc_canvas.get_tk_widget().pack(side=tk.LEFT, expand=0)

        self.fig_bloch_canvas = FigureCanvasTkAgg(fig_bloch, self.plotframe)
        self.fig_bloch_canvas.get_tk_widget().pack(side=tk.LEFT, expand=0)

    def draw(self, n_cards, deck, hand):
        if n_cards + len(hand) > 10:
            n_cards = 10 - len(hand)
        for i in range(n_cards):
            gate = random.choice(deck)
            hand.append(gate)
            deck.remove(gate)
        hand.sort()

    def show_apply(self):
        self.apply_button.pack()

    def show_radio_control2(self):
        for wire in self.radio_control2:
            wire.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.control2_lbl.pack(side=tk.TOP, fill=tk.X)

    def show_radio_control1(self, disable=[]):
        if self.target_wire.get() in disable:
            self.apply_button.pack_forget()

        for i, wire in enumerate(self.radio_control1):
            wire.pack(side=tk.TOP, fill=tk.X, expand=1)
            wire.configure(state=tk.NORMAL)
            if i in disable:
                wire.configure(state=tk.DISABLED)
        self.control1_lbl.pack(side=tk.TOP, fill=tk.X)

    def show_radio_target(self, disable=[]):
        if self.target_wire.get() in disable:
            self.apply_button.pack_forget()

        for i, wire in enumerate(self.radio_target):
            wire.pack(side=tk.TOP, fill=tk.X, expand=1)
            wire.configure(state=tk.NORMAL)
            if i in disable:
                wire.configure(state=tk.DISABLED)
        self.target_lbl.pack(side=tk.TOP, fill=tk.X)

    def show_wire_choices(self, gate):
        self.hide_wire_choices()

        if gate in ["H", "X", "Y", "Z", "S", "T"]:
            self.show_radio_target()
        elif gate in ["CX"]:
            self.show_radio_control1()
        elif gate in ["CCX"]:
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
            tk.Radiobutton(
                self.topframe,
                text=gate,
                variable=self.p1_choice,
                value=i,
                command=lambda: self.show_wire_choices(
                    self.p1_hand[self.p1_choice.get()]
                ),
            )
            # tk.Radiobutton(self.topframe, text=gate, variable=self.p1_choice, value=i, command= lambda: self.show_wire_choices(self.p1_hand[self.p1_choice.get()])).pack(side=tk.LEFT, fill=tk.X, expand=1)
            for i, gate in enumerate(self.p1_hand)
        ]
        self.lbl_p1.pack(side=tk.LEFT, fill=tk.X)
        for r in self.p1_radio:
            r.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.pass_button1.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def show_p2_choice(self):
        self.p2_radio = [
            tk.Radiobutton(
                self.bottomframe,
                text=gate,
                variable=self.p2_choice,
                value=i,
                command=lambda: self.show_wire_choices(
                    self.p2_hand[self.p2_choice.get()]
                ),
            )
            for i, gate in enumerate(self.p2_hand)
        ]
        self.lbl_p2.pack(side=tk.LEFT, fill=tk.X)
        for r in self.p2_radio:
            r.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.pass_button2.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def hide_p1_choice(self):
        self.lbl_p1.pack_forget()
        for r in self.p1_radio:
            r.destroy()
        self.pass_button1.pack_forget()

    def hide_p2_choice(self):
        self.lbl_p2.pack_forget()
        for r in self.p2_radio:
            r.destroy()
        self.pass_button2.pack_forget()

    def initial_circuit(self):
        self.qc = qiskit.QuantumCircuit(NUM_WIRES, NUM_WIRES)
        self.qc.x(range(NUM_WIRES // 2))
        self.qc.h(range(NUM_WIRES))
        self.qc.barrier()

    def board(self):
        self.hide_p1_choice()
        self.hide_p2_choice()
        self.hide_wire_choices()
        self.apply_button.pack_forget()
        if self.active_player == 1:
            self.show_p1_choice()
            if len(self.p1_hand) == 0:
                self.end_round()
        else:
            self.show_p2_choice()
            if len(self.p2_hand) == 0:
                self.end_round()

    def end_turn(self):
        if self.p1_pass and self.p2_pass:
            self.end_round()
            # self.board()
        elif self.p1_pass or self.p2_pass:
            self.board()
        else:  # change players if nobody passed
            self.active_player = (self.active_player + 1) % 2
            self.board()

    def pass_round(self):
        if self.active_player == 1:
            self.p1_pass = True
        else:
            self.p2_pass = True
        self.active_player = (self.active_player + 1) % 2
        self.end_turn()

    # def pass1(self):
    #     self.p1_pass = True
    #     self.end_turn()

    # def pass2(self):
    #     self.p2_pass = True
    #     self.active_player = (self.active_player + 1) % 2
    #     self.end_turn()

    def apply_gate(self, gate, wires):
        # print(gate, wires)
        if gate == "H":
            self.qc.h(wires[0])
        elif gate == "X":
            self.qc.x(wires[0])
        elif gate == "Y":
            self.qc.y(wires[0])
        elif gate == "Z":
            self.qc.z(wires[0])
        elif gate == "S":
            self.qc.s(wires[0])
        elif gate == "T":
            self.qc.t(wires[0])
        elif gate == "CX":
            self.qc.cnot(wires[1], wires[0])
        elif gate == "CCX":
            self.qc.toffoli(wires[2], wires[1], wires[0])

        self.p1_hand.remove(gate) if self.active_player == 1 else self.p2_hand.remove(
            gate
        )
        self.replot()
        self.end_turn()

    def win(self, wynik):
        print(wynik)

    def end_round(self):
        self.draw(3, self.p1_deck, self.p1_hand)
        self.draw(3, self.p2_deck, self.p2_hand)

        self.qc.measure(self.qc.qregs[0], self.qc.cregs[0])
        backend = Aer.get_backend("aer_simulator")
        counts = backend.run(self.qc, shots=1).result().get_counts()
        result = list(counts.keys())[0]
        measure = 0
        for i in result:
            measure += int(i)

        if measure < 3:
            self.p1_points += 1
            pointsfor = "Player 1. (There are more 0s than 1s)"
        elif measure > 3:
            self.p2_points += 1
            pointsfor = "Player 2. (There are more 1s than 0s)"
        else:
            self.p1_points += 1
            self.p2_points += 1
            pointsfor = "both players. (There are as many 0s as 1s)"

        tk.messagebox.showinfo(
            "Measurement!",
            "After 1 shot, the measurement result is: "
            + result
            + "\nPoints for: "
            + pointsfor,
        )

        self.lbl_score.config(
            text=f"Score\n Player1: {self.p1_points}\n Player2: {self.p2_points}\n Round no {self.round_no}"
        )

        if self.p1_points == 2:
            if self.p2_points == 2:
                self.win("draw")
                tk.messagebox.showinfo("Game over", "Draw!")
                self.quit()
            else:
                self.win("Player1 won")
                tk.messagebox.showinfo("Game over", "Player 1 won, congratulations!")
                self.quit()

        elif self.p2_points == 2:
            self.win("{layer2 won")
            tk.messagebox.showinfo("Game over", "Player 2 won, congratulations!")
            self.quit()
        else:  # nobody won yet
            self.round_no += 1
            self.lbl_score.config(
                text=f"Score\n Player1: {self.p1_points}\n Player2: {self.p2_points}\n Round no {self.round_no}"
            )
            self.p1_pass = False
            self.p2_pass = False
            self.initial_circuit()
            self.board()


if __name__ == "__main__":
    app = App()
    app.mainloop()
