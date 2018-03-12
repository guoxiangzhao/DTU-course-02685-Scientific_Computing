#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:29:32 2018

@author: root
"""
from numsolver import numerical_solvers
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt

# Sets Plotting parameters
font_size = 15
plt.rcParams['figure.figsize'] = (15,7)
plt.rc('font',   size=font_size)       # controls default text sizes
plt.rc('axes',  titlesize=font_size)   # fontsize of the axes title
plt.rc('axes',   labelsize=font_size)  # fontsize of the x any y labels
plt.rc('xtick',  labelsize=font_size)  # fontsize of the tick labels
plt.rc('ytick',  labelsize=font_size)  # fontsize of the tick labels
plt.rc('legend', fontsize=font_size)   # legend fontsize
plt.rc('figure', titlesize=font_size)  # # size of the figure title

# Setting up solver parameters
beta            =  3
alpha           =  0.2
x0              = np.array([0.5,0.5])
tend            = 20
numsolv1        = numerical_solvers()
numsolv1.param  = [alpha,beta]
numsolv1.x0     = x0
numsolv1.maxit  = 100
numsolv1.t      = np.array([0,tend])
numsolv1.dt     = 0.01
t               = np.arange(0,tend+0.01,0.01)
numsolv1.absTol = 10**(-8)
numsolv1.relTol = 10**(-3)
numsolv1.epstol = 0.8
absTol_as       = 10**(-8) 


def PreyPredator(t,x,params):
    # PreyPredator Implementation of the PreyPredator model
    #
    # Syntax: xdot = VanDerPol(t,x,params)
    a = params[0]
    b = params[1]
    xdot = np.zeros([2, 1])
    xdot[0] = a*(1-x[1])*x[0]
    xdot[1] = -b*(1-x[0])*x[1]
    return xdot.T[0]

def JacPreyPredator(t,x,params):
    # JACPREYPREDATOR Jacobian for the Prey Predator Equation
    #
    # Syntax: Jac = JacPreyPredator(t,x,params)
    a = params[0]
    b = params[1]
    Jac = np.zeros([2, 2])
    Jac[0,0] = a*(1-x[1])
    Jac[1,0] = b*x[1]
    Jac[0,1] = -a*x[0]
    Jac[1,1] = -b*(1-x[0])
    return Jac

def PreyPredatorfunjac(t,x,params):
    return PreyPredator(t,x,params), JacPreyPredator(t,x,params)

# Solving using the Implicit fixed step size Euler method
sol_T_pp,sol_X_pp = numsolv1.ImplicitEulerFixedStepSize(PreyPredatorfunjac)

# Solving using the adaptive Implicit Euler
a_sol_T,a_sol_X,a_ss,reject = numsolv1.ImplicitEulerAdaptiveStepSize(
                                                    PreyPredatorfunjac,
                                                    absTol_as)
# Setting up scipy solver
r = ode(PreyPredator,
        JacPreyPredator).set_integrator('vode',
                                              method='bdf',
                                              order=15)
r.set_initial_value(x0, 0).set_f_params([alpha,beta]).set_jac_params([alpha,beta])
x = [[],[]]

# Solving using the scipy solver
while r.successful() and r.t < tend:
    xn = r.integrate(r.t+0.01)
    x[0].append(xn[0])
    x[1].append(xn[1])


fig, ax = plt.subplots(2, 2, figsize=(20,10), sharex=False)
# Plotting the results
ax[0,0].plot(t[:len(x[0])], x[0],label='Scipy')
ax[0,0].plot(sol_T_pp, sol_X_pp[:,0],label='IE FS')
ax[0,0].plot(a_sol_T, a_sol_X[:,0],label='IE AS')
ax[0,0].set_title('Plot of state one Predator Prey')
ax[0,0].legend(bbox_to_anchor=(-0.3, 1), loc=2, borderaxespad=0.)

ax[0,1].plot(t[:len(x[0])], x[1],label='Scipy')
ax[0,1].plot(sol_T_pp, sol_X_pp[:,1],label='IE FS')
ax[0,1].plot(a_sol_T, a_sol_X[:,1],label='IE AS')
ax[0,1].set_title('Plot of state two Predator Prey')
ax[0,1].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

ax[1,0].plot(a_sol_X[:,0], a_sol_X[:,1],label='Scipy')
ax[1,0].plot(a_sol_X[:,0], a_sol_X[:,1],label='IE FS')
ax[1,0].plot(sol_X_pp[:,0], sol_X_pp[:,1],label='IE AS')
ax[1,0].set_title('Phase state plot')
ax[1,0].legend(bbox_to_anchor=(-0.3, 1), loc=2, borderaxespad=0.)

ax[1,1].plot(a_sol_T,np.log(a_ss),label='SS')
ax[1,1].set_title('Semi log-plot of step sizes with tolerance {}'.format(absTol_as))
ax[1,1].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()