from niODERK4 import niODERK4
import time
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np

x0 = np.array([5,-2])
tspan = [0 , 5]
dt = 0.125

def swirlSys(t, x, varargin=None):
    return np.matmul(np.array([[-0.25, 1], [-1, -0.25]]), x)

class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name,)
        print('Elapsed: %s' % (time.time() - self.tstart))

print('scipy built-in.')

with Timer():
    to = np.arange(start=tspan[0], stop=tspan[1], step=dt)
    to = np.append(to,tspan[1])
    xo = odeint(func=swirlSys, y0=x0, t=to, tfirst=True)

print('numIntegrator versions:')

with Timer():
    scheme = niODERK4(swirlSys, dt)
    [ti,xi] = scheme.integrate(tspan, x0.reshape((2,1)))

xo = np.transpose(xo)

plt.figure(1)
plt.plot(to, xo[0,:], 'g-.', to, xo[1,:], 'g-.', ti, xi[0,:], 'b-', ti, xi[1,:], 'b-')
#plt.legend('ode45','ode45','numInt','numInt');


plt.figure(2)
plt.plot(np.array([range(len(to))]).flatten(), to, 'g-.', np.array([range(len(ti))]).flatten(), ti, 'b-')
plt.show()
print('Mean timesteps (ode vs custom):');
#print([mean(diff(to)) , mean(diff(ti))]);