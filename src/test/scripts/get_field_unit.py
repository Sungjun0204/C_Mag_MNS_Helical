#!/usr/bin/env python

####################################################################
# Header
import rospy
import numpy as np
from PRM_expansion import terms, x, y, z

# Reading C data
C1 = np.loadtxt('C1.csv')
C2 = np.loadtxt('C2.csv')

# Utilizing modeled B field per unit current
B1_unit = (terms * C1).T
B2_unit = (terms * C2).T

actuation_syms = np.hstack((B1_unit, B2_unit))
