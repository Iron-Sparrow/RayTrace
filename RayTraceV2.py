import numpy as np
import time as t
import matplotlib.pyplot as plt
from uuid import uuid4, uuid5
import multiprocessing as mpr
#from pprint import pprint
from numpy import ndarray as np_array
from compyl.compyl import *

license = '''This project is currently using the MIT license but this might (and probably will) change in the future.'''

def CoordValToNP(x:float, y:float, z:float) -> np_array:
    return np.array([x, y, z])

def ValToNP(x:float, y:float, z:float) -> np_array:
    return np.array([x,y,z])

def Normalize(vector):
    return vector / np.linalg.norm(vector)

def Reflect(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def c255to1(x:int) -> float:
    if x not in range(0, 255):
        raise ValueError(f"Input not valid (0-255), {x}")
    return float(x)/255

def M_Square(x:float) -> float:
    return (x*x)

def M_Cube(x:float) -> float:
    return(x*x*x)


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
    
def Divide_Res(CPU_Cores: int, y: int) -> list:
    r = int(y % CPU_Cores)
    p = int((y - r) / CPU_Cores)
    o = 0
    lst = []
    
    if r == 0:
        for i in range(o, y, p):
            o += 1
            lst.append([i + 1, o * p])
    else:
        for i in range(o, y - p, p):
            o += 1
            if r > 0:
                r -= 1
                try:
                    lst.append([last + 1, last + 1 + p])
                    last += 1 + p
                except:
                    lst.append([i+1, o * p + 1])
                    last = o * p + 1
            else:
                try:
                    lst.append([last + 1, last + p])
                    last += p
                except:
                    lst.append([i + 1, o * p + 1])
                    last = o * p + 1
    return lst


class Material():
    def __init__(self, ambient:np_array, diffuse:np_array, specular:np_array, shininess:float, reflectiveness:float) -> None:
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        try:
            self.reflectiveness = reflectiveness * (reflectiveness > 0 and reflectiveness < 1) + 0 * (reflectiveness <= 0) + 1 * (reflectiveness >= 1)
        except:
            self.reflectiveness = None
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

screen = Screen(400, 250)
camera = Camera(CoordValToNP(0, 0, 2), 60, 0.01, 32_000)

max_depth = 8

material0 = Material(ValToNP(.18, 0, 0), ValToNP(.7, 0, 0), ValToNP(1, 1, 1), 100., M_Square(.5))
material1 = Material(ValToNP(.1, 0, 0.1), ValToNP(.7, 0, .7), ValToNP(1, 1, 1), 100., M_Square(.3))
material2 = Material(ValToNP(0, 0.123, 0), ValToNP(0, 0.6, 0), ValToNP(1, 1, 1), 100., M_Square(.7))
lightmat = Material(ValToNP(1, 1, 1), ValToNP(1, 1, 1), ValToNP(1, 1, 1), None, None)
planemat = Material(ValToNP(0.089, 0.102, 0.11), ValToNP(0, 0, 0), ValToNP(.5, .5, .5), 100, 1)
