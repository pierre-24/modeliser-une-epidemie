from typing import List, Iterator

class Compartiment:
    """Compartiment of individuals
    """
    
    def __init__(self, name: str, initial: float = 0):
        self.name = name
        self.actual = .0
        self.set_population(initial)
    
    def set_population(self, p: float):
        if not (0. <= p <= 1.):
            raise Exception('{} outside bounds for population'.format(p))
        self.actual = p


class Transition:
    """Transition between two compartiments
    """
    
    def __init__(self, source: int, target: int,  rate: float, callback):
        self.source = source
        self.target = target
        self.rate = rate
        self.callback = callback
    
    def __call__(self, t : float, source_population: float, target_population: float):
        return self.callback(t, self.rate, source_population, target_population)


class CompartimentsSimulator:
    """Simulation of compartimental dynamics
    """
    
    def __init__(self):
        self.compartiments = []
        self.transitions = []
        self.t = .0
    
    def add_compartiment(self, name: str, initial: float = 0) -> int:
        
        self.compartiments.append(Compartiment(name, initial))
        return len(self.compartiments) - 1
    
    def add_transition(self, source: int, target: int, rate: float = .01, callback = lambda t, r, sp, tp: r*sp):
        if not (0 <= source < len(self.compartiments)):
            raise Exception('source {} out of bond'.format(source))
        if not (0 <= target < len(self.compartiments)):
            raise Exception('target {} out of bond'.format(target))
        
        self.transitions.append(Transition(source, target, rate, callback))
        return len(self.transitions) - 1
    
    @staticmethod
    def rk4(f, y: List[float], t: float, dt: float):
        """Runge-Kutta integrator (https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)
        """
        
        ys = [] # solution
        yh = [] # temporary
        
        # step 1
        for i, v in enumerate(f(y, t)):
            ys.append(y[i] + dt / 6 * v)
            yh.append(y[i] + dt / 2 * v)
        
        # step 2
        for i, v in enumerate(f(yh, t + dt / 2)):
            ys[i] += dt / 3 * v
            yh[i] = y[i] + dt / 2 * v
        
        # step 3
        for i, v in enumerate(f(yh, t + dt / 2)):
            ys[i] += dt / 3 * v
            yh[i] = y[i] + dt * v
        
        # step 4
        for i, v in enumerate(f(yh, t + dt)):
            ys[i] += dt / 6 * v
        
        return ys
        
    def step(self, dt: float = 1.):
        
        # define ode
        def ode(y, t):
            dydt = [.0] * len(self.compartiments)
            
            for tr in self.transitions:
                dydti = tr(t, self.compartiments[tr.source].actual, self.compartiments[tr.target].actual)
                dydt[tr.source] -= dydti
                dydt[tr.target] += dydti
            
            return dydt
        
        y = list(c.actual for c in self.compartiments)
        
        for i, yi in enumerate(CompartimentsSimulator.rk4(ode, y, self.t, dt)):
            self.compartiments[i].set_population(yi)
        
        self.t += dt
    
    def reset(self, populations, t: float = .0):
        if len(populations) != len(self.compartiments):
            raise Exception('population sizes do not match, expected {}, got {}'.format(len(population), len(self.compartiments)))
        
        for i, p in enumerate(populations):
            self.compartiments[i].set_population(p)
        
        self.t = t
    
    def __repr__(self):
        return '{:.2f}\t{}'.format(self.t, '\t'.join('{:.4f}'.format(c.actual) for c in self.compartiments))

