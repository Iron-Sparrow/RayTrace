import numpy as np
import time 
import matplotlib.pyplot as plt
from uuid import uuid5, uuid4
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
    
class Material():
    def __init__(self, ambient:np.ndarray, diffuse:np.ndarray, specular:np.ndarray, shininess:int):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        
class Object():
    def __init__(self, name:str, x:float, y:float, z:float, emit:bool, type:str, material:Material, radius:float = None):
        self.name = name
        self.world_position = np.array([x, y, z])
        self.emit = emit
        self.type = type.lower()
        self.material = material
        sphere_list = ['sphere', 's', 'o']
        if type.lower() in sphere_list:
            if radius == None:
                raise ValueError(f"Radius can't be none.")
            else:
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

material0 = Material(ToNP(0.1, 0, 0), ToNP(.7, 0, 0), ToNP(1, 1, 1), 100)
material1 = Material(ToNP(0.1, 0, 0.1), ToNP(.7, 0, 0.7), ToNP(1, 1, 1), 100)
material2 = Material(ToNP(0, 0.1, 0), ToNP(0, 0.6, 0), ToNP(1, 1, 1), 100)
lightmat = Material(ToNP(1, 1, 1), ToNP(1, 1, 1), ToNP(1, 1, 1), 100)

sphere0 = Object("Sphere0", -2.0, 0, -1, False, 'sphere', material0,.7)
sphere1= Object("Sphere1", .1, -.3, 0, False, 'sphere', material1, .1)
sphere2 = Object("Sphere2", -.3, 0, 0, False, 'sphere', material2, .15)
sphere_list = [sphere0, sphere1, sphere2]

light0 = Object("Light0", 5, 5, 5, True, 'light', lightmat)


ot = time.time()
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
        norm_to_surface = Normalize(intersection - nearest_sphere.world_position)
        shift_point = intersection + (10 ** -5)*norm_to_surface
        intersection_to_light = Normalize(light0.world_position - shift_point)
        _, min_distance = Nearest_Intersected_Sphere(sphere_list, shift_point, intersection_to_light)
        intersection_to_light_distance = np.linalg.norm(light0.world_position - intersection)
        is_shadowed = min_distance < intersection_to_light_distance

        if is_shadowed:
            continue

        illumination = np.zeros((3))

        illumination += nearest_sphere.material.ambient * light0.material.ambient

        illumination += nearest_sphere.material.diffuse * light0.material.diffuse * np.dot(intersection_to_light, norm_to_surface)

        intersection_to_camera = Normalize(origin - intersection)
        H = Normalize(intersection_to_light + intersection_to_camera)
        illumination += nearest_sphere.material.specular * light0.material.specular * (np.dot(norm_to_surface, H) ** (nearest_sphere.material.shininess / 4))

        image[i, j]= np.clip(illumination, 0, 1)

    print("Progress: %d/%d" % (i + 1, screen.resolution[1]))

plt.imsave(f'{(uuid5(uuid4(), "Image").hex)[:8]}.png', image)
print(f"{((time.time() - ot) * 1000):.2f} ms, {(time.time() - ot):.3f} s")