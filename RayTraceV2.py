import numpy as np
import time as t
import matplotlib.pyplot as plt
from uuid import uuid4, uuid5
import multiprocessing as mpr
#from pprint import pprint
from numpy import ndarray as np_array

license = '''This project is currently using the MIT license but this might (and probably will) change in the future.'''

def CoordToNP(x, y, z):
    return np.array([x, y, z])

def Normalize(vector):
    return vector / np.linalg.norm(vector)

def Reflect(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def Sphere_Intersect(position, radius:float, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - position)
    c = np.linalg.norm(ray_origin - position) ** 2 - radius ** 2
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
    min_dist = np.inf
    for ind, dist in enumerate(distances):
        if dist and dist < min_dist:
            min_dist = dist
            nearest_sphere = sphere_list[ind]
        return nearest_sphere, min_dist
def Divide_Res():
    pass

class Material():
    def __init__(self, ambient:np_array, diffuse:np_array, specular:np_array, shininess:float, reflectiveness:float) -> None:
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflectiveness = reflectiveness * (reflectiveness > 0 and reflectiveness > 1) + 0 * (reflectiveness <= 0) + 1 * (reflectiveness >= 1)
class Object():
    def __init__(self, world_positiom:np_array, type:str, material:Material, light_intensity:float = 0, radius:float = None) -> None:
        type = type.lower()
        self.world_position = world_positiom
        self.type = type
        self.material = material
        if type == 'light':
            self.light_intensity = light_intensity
        elif type == 'sphere':
            self.radius = radius

class Screen():
    def __init__(self, x:int, y:int) -> None:
        self.resolution = x,y
        self.aspect_ratio = float(x)/y
        self.ar = float(x)/y
        if self.ar != self.aspect_ratio:
            raise ValueError("Problem with Screem, aspect-ratio mismatch")
        self.left = -1.0
        self.right = 1.0
        self.top = 1.0 / self.ar
        self.bottom = -1.0 / self.ar
        self.x = x
        self.y = y

class Camera():
    def __init__(self, world_position:np_array, fov:float, near:float, far:int) -> None:
        self.world_position = world_position
        self.fov = fov
        self.near = near
        self.far = float(far)
