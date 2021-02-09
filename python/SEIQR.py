import math

from dynamic.model import CompartimentsSimulator

seir = CompartimentsSimulator()
S = seir.add_compartiment('S', .99)
E = seir.add_compartiment('E')
I = seir.add_compartiment('I', .01)
Q = seir.add_compartiment('Q')
R = seir.add_compartiment('R')

t_SE = seir.add_transition(S, E, .2, lambda t, r, sp, tp: r*sp*seir.compartiments[I].actual)  # tweak
t_EI = seir.add_transition(E, I, .05)
t_EQ = seir.add_transition(E, Q, .01)
t_IR = seir.add_transition(I, R, .1)
t_QR = seir.add_transition(Q, R, .14)

dt = .01
tprint = int(1 / dt)
n = 0
time = 500
while abs(time - seir.t) >= dt:
    seir.step(dt)
    n += 1
    if n % tprint == 0:
        print(seir)
