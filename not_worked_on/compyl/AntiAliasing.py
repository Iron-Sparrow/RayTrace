#imports
import numba
from math import sqrt, pi
import numpy as np
from random import random, randint

#constants
##SMAA
SMAA_LEVEL_NONE = 0
SMAA_LEVEL_LOW = 1
SMAA_LEVEL_HIGH = 2
##SSAA
SSAA_LEVEL_NONE = 0
SSAA_LEVEL_BASIC = 1
SSAA_LEVEL_LOW = 2
SSAA_LEVEL_MEDIUM = 3
SSAA_LEVEL_HIGH = 4
SSAA_LEVEL_VERY_HIGH = 5
SSAA_LEVEL_ULTRA = 6
##

#Functions
@numba.njit(fastmath=True)
def Clamp(x, minf, maxf):
    return (x * (x > minf) * (x < maxf) + minf * (x <= minf) + maxf * (x >= maxf))

def RPAA(r:float, n:int):
    if n < 2:
        if n == 1:
            raise ValueError(f"You should use ROAA with n={n}")
        else:
            raise ValueError(f"n = {n} not valid. Please use a strictly higher than 1")
    r = (sqrt(Clamp(r, 0, 1))/2)
    step = 2*pi/n
    

def SSAA(level:int):
    if level == SSAA_LEVEL_NONE:
        pass

def SMAA(level:int):
    if level == SMAA_LEVEL_NONE:
        pass
    else:
        sub = (level + 1) ** 2
    
def ROAA():
    #RPAA but with one n
    pass
