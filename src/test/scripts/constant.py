#!/usr/bin/env python

####################################################################
# Header
import rospy
import numpy as np

# Theta, angle between axis of symmetry and x-axis
th = np.pi/2

# Phi, angle between axis of symmetry and y-axis
ph = 0

# Delta, angle between axis of symmetry and magnetization                                     
dl = np.pi/2

# Resistance of each coil                  
R = np.array([[6.07, 6.14]])

# Operating point
P = np.array([0, 0, 0])

# Desired field magnitude
B_amp = 10

# Desired field rotating frequency
freq = 1