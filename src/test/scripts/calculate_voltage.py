#!/usr/bin/env python

####################################################################
# Header
import rospy
import numpy as np
import sympy as sp
from scipy.linalg import pinv
from constant import *
from get_field_unit import actuation_syms, x, y, z

# 
f = sp.lambdify((x, y, z), actuation_syms)
actuation = np.array(f(P[0], P[1], P[2]))

# N, unit vector directs axis of symmetry
N = np.array([np.cos(th),
              np.sin(th)*np.cos(ph),
              np.sin(th)*np.sin(ph)])

# U, unit vector perpendicular to N
U = np.array([np.sin(th),
              -np.cos(th)*np.cos(ph),
              -np.cos(th)*np.sin(ph)])


# U_length = np.sqrt(((U[0]**2)-(N[0]**2)) + ((U[1]**2)-(N[1]**2)) + ((U[2]**2)-(N[2]**2)))
# N_length = np.sqrt((N[0]**2) + (N[1]**2) + (N[2]**2))

# dl = np.arctan2(N_length, U_length)


def B_R(t):
    return (B_amp * (np.cos(dl)*N + 
                    np.sin(dl)*np.cos(2*np.pi*freq*t)*U + 
                    np.sin(dl)*np.sin(2*np.pi*freq*t)*np.cross(N,U)
                    ))[:, np.newaxis]

def I(t):
    return pinv(actuation).dot(B_R(t))

def V(t):
    return I(t).T * R