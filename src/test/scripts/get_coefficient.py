#!/usr/bin/env python

####################################################################
# Header
import rospy
import numpy as np
import pandas as pd
import sympy as sp
from scipy.linalg import pinv
from PRM_expansion import H, terms, x, y, z

# Rotation matrix
def rot_z(AoR):
    return np.array([[+np.cos(AoR), -np.sin(AoR), 0],
                     [+np.sin(AoR), +np.cos(AoR), 0],
                     [0, 0, 1]])

# Precondition
sim_data = pd.read_csv('ROI_matrix.csv', header = None).values
N = len(sim_data)
AoR = [0, np.pi] # angle of rotation

# Initialization
A_mat = np.zeros((N, H))
C = np.zeros((2, H, 3))

# Utilizing coefficient matrix C
for a in range(2):
    pos = (rot_z(AoR[a]).dot(sim_data[:, 0:3].T)).T
    B_sim = (rot_z(AoR[a]).dot(sim_data[:, 3:6].T)).T

    for b in range(N):
        f = sp.lambdify((x, y, z), terms)
        A_mat[b, :] = f(pos[b, 0], pos[b, 1], pos[b, 2])

    C_x = pinv(A_mat).dot(B_sim[:, 0])
    C_y = pinv(A_mat).dot(B_sim[:, 1])
    C_z = pinv(A_mat).dot(B_sim[:, 2])

    C[a] = np.array([C_x, C_y, C_z]).T

# Saving C data
np.savetxt('C1.csv', C[0])
np.savetxt('C2.csv', C[1])

