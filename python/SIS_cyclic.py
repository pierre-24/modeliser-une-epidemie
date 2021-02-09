import math

from typing import Callable, Tuple
from dynamic.model import CompartimentsSimulator


# make cyclic SIS
def cyclic_rate(t: float, rmax: float, rmin: float = .01, T: float = 100) -> float:
    return rmin + .5*(1 + math.sin(t/T * math.pi * 2)) * (rmax-rmin)

sis = CompartimentsSimulator()
S = sis.add_compartiment('S', .99)
I = sis.add_compartiment('I', .01)

t_SI = sis.add_transition(S, I, .2, lambda t, r, sp, tp: cyclic_rate(t, r)*sp*tp)
t_IS = sis.add_transition(I, S, .1)


dt = .01
tprint = int(1 / dt)
n = 0
time = 2000
while abs(time - sis.t) >= dt:
    sis.step(dt)
    n += 1
    if n % tprint == 0:
        print(sis, end='\t')
        print(cyclic_rate(sis.t, .2))
