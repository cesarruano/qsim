import numpy as np
from logger import *

#array that represents gates
class Q_array:
    def __init__(self):
        self.dimension = 2
        self.array = np.identity(self.dimension)
        self.name = "I"
    def conj(self):
        conj_gate = Q_array()
        conj_gate.dimension = self.dimension
        conj_gate.array = self.array.conj().T
        conj_gate.name = self.name+"*"
    def display(self):
        print self.name+":"
        print self.array


global I_gate
I_gate = Q_array()

global H_gate
H_gate = Q_array()
H_gate.array = np.array([[1,1],[1,-1]])/np.sqrt(2)
H_gate.name = "H"

global S_gate
S_gate = Q_array()
S_gate.array = np.array([[1,0],[0,1j]])
S_gate.name = "S"

global X_gate
X_gate = Q_array()
X_gate.array = np.array([[0,1],[1,0]])
X_gate.name = "X"

global Y_gate
Y_gate = Q_array()
Y_gate.array = np.array([[0,-1j],[1j,0]])
Y_gate.name = "Y"

global Z_gate
Z_gate = Q_array()
Z_gate.array = np.array([[1,0],[0,-1]])
Z_gate.name = "Z"

global T_gate
T_gate = Q_array()
T_gate.array = np.array([[1,0],[0,(1+1j)/np.sqrt(2)]])
T_gate.name = "T"

global CNOT_gate
CNOT_gate = Q_array()
CNOT_gate.array = np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
CNOT_gate.name = "CNOT"

global gates
gates = [I_gate, H_gate, S_gate, X_gate, Y_gate, Z_gate, T_gate, CNOT_gate]

def display_available_gates():
    print "Available gates:\n"
    for g in gates:
        g.display()
        print "\n"

def build_full_array_1q(system, subarray, qbit):
    if qbit+1 > system.qbits:
        log(error, "qbit "+str(qbit)+" out of range in system with "+str(system.qbits)+" qbits")
    result = np.array([1])
    for i in range(0, system.qbits):
        current_array = I_gate.array
        if qbit==i:
            current_array = subarray
        result=np.kron(current_array, result)
    return result

def build_full_array_nq(system, subarray):
    result = subarray
    for i in range(0, system.qbits-int(np.sqrt(len(subarray)))):
        result=np.kron(I_gate.array, result)
    return result

def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

def convert_to_base(num, base):
    log(debug_level, "Converting "+str(num)+" to base "+str(base))
    bits=bitfield(num)
    bits.reverse()
    result = 0
    exp = 0
    for i in range(0,len(bits)):
        result = result + (2**base[i])*bits[i]
    return result

def qbit_new_base_array(system, base):
    log(debug_level, "Calculating new base array from base "+str(base)+" for system "+system.name)
    result_array = np.identity(system.array_size)
    helper_array = np.identity(system.array_size)
    for i in range(0,system.array_size):
        result_array[i]=helper_array[convert_to_base(i, base)]
    return result_array


def G1(system, qbit, array):
    full_transform=build_full_array_1q(system, array, qbit)
    system.accumulated_transform=np.dot(full_transform,system.accumulated_transform)
    system.state = np.dot(full_transform,system.state)

def Gn(system, qbits, array):
    log(debug_level, "Applying block gate with array \n"+str(array)+"\n to qbits "+str(qbits))
    base_free_transform=build_full_array_nq(system, array)
    unused_qbits = list(set(range(0,system.qbits)) - set(qbits))
    log(debug_level, "Used qbits: "+str(qbits))
    log(debug_level, "Unused qbits: "+str(unused_qbits))
    new_base = qbits+unused_qbits
    log(debug_level, "New base: "+str(new_base))
    base_change_array = qbit_new_base_array(system, new_base)
    actual_base_transform = np.dot(base_change_array,np.dot(base_free_transform,base_change_array))
    system.accumulated_transform=np.dot(actual_base_transform,system.accumulated_transform)
    system.state = np.dot(actual_base_transform,system.state)
    log(debug_level, "Base change:\n"+str(base_change_array))
    log(debug_level, "Normal base transform:\n"+str(base_free_transform))
    log(debug_level, "Actual base transform:\n"+str(actual_base_transform))

def H(system, qbit):
    log(debug_level, "Apply H gate on qbit "+str(qbit)+" on "+str(system.name))
    G1(system, qbit, H_gate.array)

def S(system, qbit):
    log(debug_level, "Apply S gate on qbit "+str(qbit)+" on "+str(system.name))
    G1(system, qbit, S_gate.array)

def I(system, qbit):
    log(debug_level, "Apply I gate on qbit "+str(qbit)+" on "+str(system.name))
    G1(system, qbit, I_gate.array)

def X(system, qbit):
    log(debug_level, "Apply X gate on qbit "+str(qbit)+" on "+str(system.name))
    G1(system, qbit, X_gate.array)

def Y(system, qbit):
    log(debug_level, "Apply Y gate on qbit "+str(qbit)+" on "+str(system.name))
    G1(system, qbit, Y_gate.array)

def Z(system, qbit):
    log(debug_level, "Apply Z gate on qbit "+str(qbit)+" on "+str(system.name))
    G1(system, qbit, Z_gate.array)

def T(system, qbit):
    log(debug_level, "Apply T gate on qbit "+str(qbit)+" on "+str(system.name))
    G1(system, qbit, T_gate.array)

def CNOT(system, c_qbit, o_qbit):
    log(debug_level, "Apply CNOT gate on qbit"+str(o_qbit)+" with control qbit"+str(c_qbit)+" on "+str(system.name))
    Gn(system, [c_qbit, o_qbit], CNOT_gate.array)
