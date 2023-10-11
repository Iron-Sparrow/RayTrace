import numpy as np
import time as t
import matplotlib.pyplot as plt
from uuid import uuid4, uuid5
import multiprocessing as mpr
#from pprint import pprint

license = '''This project is currently using the MIT license but this might (and probably will) change in the future.'''

def ToNP(x, y, z):
    return np.array([x, y, z])

def Normalize(vector):
    return vector / np.linalg.norm(vector)

def Reflect(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def Sphere_Intersect(position, radius:float, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - position)
    c = np.linalg.norm(ray_origin - origin) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta >= 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None

def Nearest_Intersected_Sphere(sphere_list:list, ray_origin, ray_direction):
    distances =[]
    for sphere in sphere_list:
       distances.append(Sphere_Intersect(sphere.world_position, sphere.radius, ray_origin, ray_direction)) 
    nearest_sphere = None
def Divide_Res():
    pass
