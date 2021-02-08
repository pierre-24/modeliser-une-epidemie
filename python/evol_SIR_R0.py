import math
import numpy

from typing import Callable, Tuple
from dynamic.model import CompartimentsSimulator


# find extremum
golden_ratio = (math.sqrt(5) + 1) / 2

def find_extremum(f: Callable, interval: Tuple[float, float], threshold: float = 1e-5, find_max: bool = True) -> Tuple[float, float]: 
    """Find the extremum of `f` inside the `interval` using the golden section search
    (https://en.wikipedia.org/wiki/Golden-section_search)
    """
    
    length = interval[1] - interval[0]
    
    if abs(length) < threshold:
        x = (interval[0] + interval[1]) / 2
        return x, f(x)
    else:
        c = interval[1] - length / golden_ratio
        fc = f(c)
        d = interval[0] + length / golden_ratio
        fd = f(d)
        
        new_interval = (c, interval[1])
        if (find_max and fc > fd) or (not find_max and fc < fd):
            new_interval = (interval[0], d)
        
        return find_extremum(f, new_interval, threshold, find_max)

def find_root(f: Callable, x0: float, x1: float, threshold: float = 1e-5) -> float:
    """Find a root using the Secant method (a kind of finite difference  approximation)
    (https://en.wikipedia.org/wiki/Secant_method)
    """
    
    # print(x0, x1)
    
    fx1 = f(x1)
    
    if abs(fx1) < threshold:
        return x1
    else:
        fx0 = f(x0)
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        return find_root(f, x1, x2, threshold)

# make SIR
sir = CompartimentsSimulator()
S = sir.add_compartiment('S', .99)
I = sir.add_compartiment('I', .01)
R = sir.add_compartiment('R')

t_SI = sir.add_transition(S, I, .2, lambda t, r, sp, tp: r*sp*tp)
t_IR = sir.add_transition(I, R, .1)

def It(t: float, R0: float, gamma: float = .1, I0: float = .01, dt: float = .01):
    """Compute infected population at a given t. Since this requires at least S(t), do the actual simulation
    """
    
    # set the correct transition
    sir.transitions[t_SI].rate = R0 * gamma
    sir.transitions[t_IR].rate = gamma
    
    # compute until t:
    sir.reset([1-I0, I0, 0])
    while sir.t < t:
        sir.step(dt)
        
    # get value
    return sir.compartiments[I].actual

def Ipc(pc: float, R0: float, t_max_I: float, gamma: float = .1, I0: float = .01, dt: float = .01):
    """Find when the models goes below an infected rate of `pc` %
    """
    # set the correct transition
    sir.transitions[t_SI].rate = R0 * gamma
    sir.transitions[t_IR].rate = gamma
    
    # compute until t:
    sir.reset([1-I0, I0, 0])
    while sir.t < t_max_I or sir.transitions[t_SI](sir.t, sir.compartiments[S].actual, sir.compartiments[I].actual) > pc:
        # print(sir.t, sir.transitions[t_SI](sir.t, sir.compartiments[S].actual, sir.compartiments[I].actual))
        sir.step(dt)
        
    # get value
    return sir.t


def Sinf(St: float, R0: float, S0: float = .99):
    return math.log(St / S0) - R0 * (St - 1)

print('R0\tt_max\tI_max\tHerd\tSinf\tt_1%')
for R0 in numpy.arange(1.1, 7.6, .1):
    max_I = find_extremum(lambda x: It(x, R0), (0, 100), find_max=True)
    herd = 1 - 1/R0
    Sinf_ = find_root(lambda x: Sinf(x, R0), .001, .002) # this fails for R0>7.5 since it requires to evaluate ln(0)
    t01pc = Ipc(.001, R0, max_I[0])
   
    print('{:.2f}\t{:.1f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}'.format(R0, *max_I, herd, Sinf_, t01pc))

