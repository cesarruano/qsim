import numpy as np
from qsim_gates import *

global default_state

#initial state |0...0>

class Q_system:
    def __init__(self, qbits, name="Anonymous System"):
        self.qbits = qbits
        self.array_size = 2**qbits
        self.accumulated_transform = np.identity(self.array_size)
        default_state = np.zeros([self.array_size, 1])
        default_state[0] = 1
        self.state = default_state
        self.name = name
    def __str__(self):
        result=str(self.name)+":\n\n"
        result += "System state:\n"+str(self.state)
        result += "\nSystem state (no phase):\n"+str(self.no_phase())
        result += "\nAccumulated transform:\n"+str(self.accumulated_transform)+"\n"
        return result

    def no_phase(self):
        #if self.state[0]==0:
        log(debug_level, "Extracting phase\n"+str(self.state))
        aux = 0+0j
        aux = aux+self.state[0]
        return self.state*\
                    (\
                        aux.conjugate()\
                            /\
                        ((np.sqrt(aux.conjugate()*aux)) ) )
