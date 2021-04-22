import numpy as np
from ODESolver import ForwardEuler
from matplotlib import pyplot as plt
from scipy.integrate import odeint

"""
N = 11376070

I0, R0 = 3448, 3409

S0 = N - I0 - R0

beta, gamma = 0.083, 0.841

t = np.linspace(0, 160, 160)

def deriv(y, t, N, beta, gamma):
    S,I,_ = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

y0 = S0, I0, R0
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S/1000, 'b', label='Susceptible')
ax.plot(t, I/1000, 'r', label='Infected')
ax.plot(t, R/1000, 'g', label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')

ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)

plt.show()


"""

class SIR:
    def __init__(self, nu, beta, S0, I0, R0):

        if isinstance(nu, (float, int)):
            self.nu = lambda t: nu
        elif callable(nu):
            self.nu = nu
        
        if isinstance(beta, (float, int)):
            self.beta = lambda t: beta
        elif callable(beta):
            self.beta = beta

        self.initial_conditions = [S0, I0, R0]

    def __call__(self, u, t):

        S, I, _ = u

        return np.asarray([

            -self.beta(t) * ((S * I) / (self.initial_conditions[0] + self.initial_conditions[1] + self.initial_conditions[2])), 
            self.beta(t) * ((S * I) / (self.initial_conditions[0] + self.initial_conditions[1] + self.initial_conditions[2])) - self.nu(t) * I,
            self.nu(t) * I

        ])


if __name__ == '__main__':
    
    sir = SIR(0.14, 0.94, 15000, 400, 350)

    solver =  ForwardEuler(sir)
    solver.set_initial_conditions(sir.initial_conditions)

    time_steps = np.linspace(0, 60, 10001)
    u, t = solver.solve(time_steps)

    plt.plot(t, u[:, 0], label='susceptible')
    plt.plot(t, u[:, 1], label='infected')
    plt.plot(t, u[:, 2], label='recovered')
    plt.legend()

    plt.show()