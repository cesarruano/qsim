import numpy as np
from qsim_gates import *
from qsim_system import *
from logger import *
from qsim_about import *

display_program_header()
display_available_gates()

system = Q_system(2, name="SYSTEM1")

print system

H(system, 0)
S(system, 0)
S(system, 0)
H(system, 0)

#T(system, 0)
print ""
print system

def groover():
    H(system, 0)
    H(system, 1)

    S(system, 0)
    S(system, 1)

    H(system, 1)

    CNOT(system,0,1)

    H(system, 1)

    S(system, 0)
    S(system, 1)
