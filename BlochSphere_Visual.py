import tkinter as tk
from tkinter import *
import os, time, math, numpy as np
from qiskit import *
from qiskit.tools.visualization import plot_histogram, plot_bloch_multivector

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

class BSVector:
    def __init__(self):
        self.state_vector = np.array([1+0j, 0+0j])
        #https://qiskit.org/textbook/ch-gates/quantum-gates.html

        self.x = np.array([[0,1],[1,0]])
        self.y = np.array([[0,0-1j],[0+1j,0]])
        self.z = np.array([[1,0],[0,-1]])

        self.h = np.array(1/math.sqrt(2)) * np.array([[1,1],[1,-1]])
        self.s = np.array([[1,0],[0,0+1j]])
        self.sdg = np.array([[1,0],[0,0-1j]])

        self.t = np.array([[1,0],[0,math.e**(0+1j*(math.pi/4))]])
        self.tdg = np.array([[1,0],[0,math.e**(0-1j*(math.pi/4))]])

        self.update_theta(None)

    def qgate(self, gate):
        if not isinstance(gate, str):
            self.state_vector = self.state_vector @ gate
        else:
            self.state_vector = np.array([1+0j, 0+0j])

        fig = plot_bloch_multivector(self.state_vector)
        fig_mpl = FigureCanvasTkAgg(fig, f_mpl)
        fig_mpl._tkcanvas.grid(row = 0, column = 0, sticky = "n")
        plt.close(fig)

        c = []
        for n in self.state_vector.tolist():
            c.append(f"{round(n.real, 2)} + {round(n.imag, 2)}j")

        state_out = f"[{c[0]}, {c[1]}]"
        l_state_v.configure(text = f"State Vector: {state_out}")

    def update_theta(self, event):
        if event != None:
            self.theta = s_theta.get()
            try:
                e_theta_e = float(e_theta.get())
                if rad_deg_o.get() == "Rad":
                    e_theta_e = np.degrees(e_theta_e)

                self.theta = e_theta_e
                s_theta.set(e_theta_e)
            except:
                pass
            e_theta.delete(0, END)
            l_other.configure(text = f"Other:     Theta (Deg/Rad): {round(self.theta,2)}, {round(np.radians(self.theta),4)}")
        else: self.theta = 0
        
        self.th_rad = np.radians(self.theta)

        self.rx = np.array([[math.cos(self.th_rad/2),0-1j*math.sin(self.th_rad/2)],[0-1j*math.sin(self.th_rad/2),math.cos(self.th_rad/2)]])
        self.ry = np.array([[math.cos(self.th_rad/2),-1*math.sin(self.th_rad/2)],[math.sin(self.th_rad/2),math.cos(self.th_rad/2)]])
        self.rz = np.array([[math.e**(0-1j*self.th_rad/2),0],[0,math.e**(0+1j*self.th_rad/2)]])

win = tk.Tk()
win.title("Bloch Sphere Visual")
win.minsize(150, 100)

win.columnconfigure([0,1], pad = 10)

info = Frame(win)
info.grid(row = 0, column = 0, sticky = "n")

info.rowconfigure([1,2], pad = 10)
info.columnconfigure(0, pad = 10)

f_mpl = Frame(win, borderwidth = 2, relief=GROOVE)
f_mpl.grid(row = 0, column = 1, sticky = "n", pady = 5)

l_state_v = Label(info, text="State Vector:", width = 50, height = 1, anchor = "w", relief=GROOVE)
l_state_v.grid(row = 0, column = 0, pady = 5)
b_reset = Button(info, text="RESET", width = 50, command = lambda: V.qgate("reset")).grid(row = 1, column = 0)

V = BSVector()
fig = plot_bloch_multivector(V.state_vector)
V.qgate("reset")

operators = Frame(info)
operators.rowconfigure([0,1], pad = 10)
operators.grid(row = 2, column = 0, sticky = "n")

pauli = Frame(operators, borderwidth = 2, relief=GROOVE)
pauli.grid(row = 0, column = 0, sticky = "n")

hadamard = Frame(operators, borderwidth = 2, relief=GROOVE)
hadamard.grid(row = 1, column = 0, sticky = "n")

other = Frame(operators, borderwidth = 2, relief=GROOVE)
other.grid(row = 2, column = 0, sticky = "n")

#Pauli
l_pauli = Label(pauli, text="Pauli Operators:", width = 50, height = 1, anchor = "w").grid(row = 0, column = 0)
pauli_gates = Frame(pauli)
pauli_gates.columnconfigure([0,1,2], pad = 10)
pauli_gates.rowconfigure(0, pad = 10)
pauli_gates.grid(row = 1, column = 0)

b_x_gate = Button(pauli_gates, text = "X", width = 3, command = lambda: V.qgate(V.x)).grid(row = 0, column = 0)
b_y_gate = Button(pauli_gates, text = "Y", width = 3, command = lambda: V.qgate(V.y)).grid(row = 0, column = 1)
b_z_gate = Button(pauli_gates, text = "Z", width = 3, command = lambda: V.qgate(V.z)).grid(row = 0, column = 2)

#H S
l_hadamard = Label(hadamard, text="Hadamard and S:", width = 50, height = 1, anchor = "w").grid(row = 0, column = 0)
hadamard_gates = Frame(hadamard)
hadamard_gates.columnconfigure([0,1,2], pad = 10)
hadamard_gates.rowconfigure(0, pad = 10)
hadamard_gates.grid(row = 1, column = 0)

b_h_gate = Button(hadamard_gates, text = "H", width = 3, command = lambda: V.qgate(V.h)).grid(row = 0, column = 0)
l_p = Label(hadamard_gates, width = 1).grid(row = 0, column = 1)
b_s_gate = Button(hadamard_gates, text = "S", width = 3, command = lambda: V.qgate(V.s)).grid(row = 0, column = 2)
b_sdg_gate = Button(hadamard_gates, text = "Sdg", width = 3, command = lambda: V.qgate(V.sdg)).grid(row = 0, column = 3)

#Other
other_info = Frame(other)
other_info.grid(row = 0, column = 0, sticky = "w")

l_other = Label(other_info, text=f"Other:     Theta (Deg/Rad): {V.theta}, {np.radians(V.theta)}", width = 30, height = 1, anchor = "w")
l_other.grid(row = 0, column = 0)
other_gates = Frame(other)
other_gates.columnconfigure([0,1,2,3,4,5], pad = 10)
other_gates.rowconfigure(0, pad = 10)
other_gates.grid(row = 2, column = 0)

s_theta = Scale(other, from_=0, to=360, tickinterval=90, orient=HORIZONTAL, length=350)
s_theta.grid(row = 1, column = 0)
win.bind("<ButtonRelease-1>", V.update_theta)
win.bind('<Return>', V.update_theta)
b_t_gate = Button(other_gates, text = "T", width = 3, command = lambda: V.qgate(V.t)).grid(row = 0, column = 0)
b_tdg_gate = Button(other_gates, text = "Tdg", width = 3, command = lambda: V.qgate(V.tdg)).grid(row = 0, column = 1)

l_theta = Label(other_info, text = "Theta:").grid(row = 0, column = 1)

e_theta = Entry(other_info, width = 5)
e_theta.grid(row = 0, column = 2)

rad_deg_o = StringVar(win)
choices_rad_deg = {'Deg','Rad'}
rad_deg_o.set('Deg')
o_theta = OptionMenu(other_info, rad_deg_o, *choices_rad_deg)
o_theta.grid(row = 0, column = 3)

l_p = Label(other_gates, width = 1).grid(row = 0, column = 2)
b_rx_gate = Button(other_gates, text = "Rx", width = 3, command = lambda: V.qgate(V.rx)).grid(row = 0, column = 3)
b_ry_gate = Button(other_gates, text = "Ry", width = 3, command = lambda: V.qgate(V.ry)).grid(row = 0, column = 4)
b_rz_gate = Button(other_gates, text = "Rz", width = 3, command = lambda: V.qgate(V.rz)).grid(row = 0, column = 5)

win.mainloop()