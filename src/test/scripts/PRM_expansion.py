#!/usr/bin/env python

####################################################################
# Header
import rospy
import sympy as sp

# Precondition
n = 5  # n-th degree polynomial
H = sp.binomial(n + 3, 3)  # number of terms

# Initialization
index = 0
x, y, z = sp.symbols('x y z')  # symbolic variables
terms = sp.zeros(1, H)  # 1xH symbolic array

# Expansion algorithm
for exp_x in range(n + 1):
    for exp_y in range(n + 1):
        for exp_z in range(n + 1):
            if exp_x + exp_y + exp_z <= n:
                terms[index] = x**exp_x * y**exp_y * z**exp_z
                index += 1