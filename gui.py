import tkinter as tk
from turtle import left
import matplotlib
import qiskit

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Matplotlib Demo')

        num_wires = 5

        # for plot
        leftframe = tk.Frame(self)
        leftframe.pack(side='left')

        # for choosing wires
        rightframe = tk.Frame(self)
        rightframe.pack(side='right', fill='both', expand=True)

        # for choosing gates
        bottomframe = tk.Frame(self)
        bottomframe.pack(side=tk.BOTTOM, fill='both', expand=True)

        qc = qiskit.QuantumCircuit(num_wires,num_wires)
        qc.h(range(num_wires))
        qc.cnot(0,1)
        for i in range(10):
            qc.h(2)

        figure = qc.draw("mpl")
        figure.set_size_inches(6, 4)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, leftframe)

        figure_canvas.get_tk_widget().pack(side=tk.LEFT, expand=0)


        for i in range(num_wires):
            tk.Radiobutton(rightframe, text=str(i), variable=None, value=i).pack(side=tk.TOP, fill=tk.X, expand=1)

        for i in range(10):
            tk.Button(bottomframe, text="H").pack(side=tk.LEFT, fill=tk.X, expand=1)

        tk.Button(self, text='Quit', command=self.quit).pack()

if __name__ == '__main__':
    app = App()
    app.mainloop()