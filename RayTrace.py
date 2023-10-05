import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from uuid import uuid5
import os

def ToNP(x, y, z):
    return np.array([x,y,z])

def Normalize(vector):
    return vector / np.linalg.norm(vector)

def Sphere_Intersect(position, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - position)
    c = np.linalg.norm(ray_origin - position) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        return min(t1, t2)
    return  None

def Nearest_Intersected_Sphere(spheres:list, ray_origin, ray_direction):
    distances = [Sphere_Intersect(sphere.world_position, sphere.radius, ray_origin, ray_direction) for sphere in spheres]
    nearest_sphere = None
    min_dist = np.inf
    for ind, dist in enumerate(distances):
        if dist and dist < min_dist:
            min_dist = dist
            nearest_sphere = spheres[ind]
        return nearest_sphere, min_dist
class Object():
    def __init__(self, name:str, x:float, y:float, z:float, emit:bool, type:str, radius:float = 0.0):
        self.name = name
        self.world_position = np.array([x, y, z])
        self.emit = emit
        self.type = type.lower()
        sphere_list = ['sphere', 's', 'o']
        if type.lower() in sphere_list:
            self.radius = radius
        
class Screen():
    def __init__(self, x:float, y:float):
        self.resolution = x, y
        self.ratio = x/y
        self.left = -1.0
        self.right = 1.0
        self.top = 1.0 / (float(x)/y)
        self.bottom = -1.0 / (float(x)/y)


class Camera():
    def __init__(self, x:float, y:float, z:float, fov:float, near:float, far:int):
        self.world_position = np.array([x, y, z])
        self.fov = fov
        self.near = near
        self.far = float(far)
                
screen = Screen(576, 360)
camera = Camera(0, 0, 1, 60.0, 0.01, 100)
sphere0 = Object("Sphere0", -2.0, 0, -1, False, 'sphere', .7)
sphere1= Object("Sphere0", .1, -.3, 0, False, 'sphere', .1)
sphere2 = Object("Sphere0", -.3, 0, 0, False, 'sphere', .15)
sphere_list = [sphere0, sphere1, sphere2]

image = np.zeros((screen.resolution[1], screen.resolution[0], 3))
for i, y in enumerate(np.linspace(screen.top, screen.bottom, screen.resolution[1])):
    for j, x in enumerate(np.linspace(screen.left, screen.right, screen.resolution[0])):
        pixel = ToNP(x, y, 0)
        origin = camera.world_position
        direction = Normalize(pixel - origin)

        nearest_sphere, min_distance = Nearest_Intersected_Sphere(sphere_list, origin, direction)
        if nearest_sphere is None:
            continue

        intersection = origin + min_distance * direction

    pprint("Progress. %d/%d" % (i + 1, screen.resolution[1]))

plt.imsave('image.png', image)