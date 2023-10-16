compyl_imported = True

import numpy as np
import matplotlib.pyplot as plt
from uuid import uuid5, uuid4
from numpy import ndarray

def CoordToNP(x:float, y:float, z:float) -> ndarray:
    return np.array([x, y, z])

def ValToNP(x:float, y:float, z:float) -> ndarray:
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
    distances = [Sphere_Intersect(sphere.world_position, sphere.radius, ray_origin, ray_direction)for sphere in sphere_list]
    nearest_sphere = None
    min_dist = np.inf
    for ind, dist in enumerate(distances):
        if dist and dist < min_dist:
            min_dist = dist
            nearest_sphere = sphere_list[ind]
    return nearest_sphere, min_dist
    
def Divide_Res(cores: int, y: int) -> list:
    r = int(y % cores)
    p = int((y - r) / cores)
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
    def __init__(self, ambient:ndarray, diffuse:ndarray, specular:ndarray, shininess:float, reflectiveness:float) -> None:
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        try:
            self.reflectiveness = reflectiveness * (reflectiveness > 0 and reflectiveness < 1) + 0 * (reflectiveness <= 0) + 1 * (reflectiveness >= 1)
        except:
            self.reflectiveness = None
class Object():
    def __init__(self, world_positiom:ndarray, tpe:str, material:Material, light_intensity:float = 0, radius:float = None) -> None:
        tpe = tpe.lower()
        self.world_position = world_positiom
        self.type = tpe
        self.material = material
        if tpe == 'light':
            self.light_intensity = light_intensity
        elif tpe == 'sphere':
            self.radius = radius

class Screen():
    def __init__(self, x:int, y:int) -> None:
        self.resolution = x, y
        self.aspect_ratio = float(x)/y
        self.ar = float(x)/y
        if self.ar != self.aspect_ratio:
            raise ValueError("Problem with Screem, aspect-ratio mismatch")
        self.left = -1.0
        self.right = 1.0
        self.top = 1.0 / (float(x)/y)
        self.bottom = -1.0 / (float(x)/y)
        self.x = x
        self.y = y

class Camera():
    def __init__(self, world_position:ndarray, fov:float, near:float, far:int) -> None:
        self.world_position = world_position
        self.fov = fov
        self.near = near
        self.far = float(far)

def Render():
    screen = Screen(400, 250)
    camera = Camera(CoordToNP(0, 0, 2), 60, 0.01, 32_000)

    max_depth = 8

    material0 = Material(ValToNP(.18, 0, 0), ValToNP(.7, 0, 0), ValToNP(1, 1, 1), 100., M_Square(.5))
    material1 = Material(ValToNP(.1, 0, 0.1), ValToNP(.7, 0, .7), ValToNP(1, 1, 1), 100., M_Square(.3))
    material2 = Material(ValToNP(0, 0.123, 0), ValToNP(0, 0.6, 0), ValToNP(1, 1, 1), 100., M_Square(.7))
    lightmat = Material(ValToNP(1, 1, 1), ValToNP(1, 1, 1), ValToNP(1, 1, 1), 100, 1)
    planemat = Material(ValToNP(0.189, 0.202, 0.21), ValToNP(0.4, 0.4, 0.4), ValToNP(.5, .5, .5), 100, 1)
    sphere0 = Object(CoordToNP(-2.0, 0, -1), 'sphere', material0, radius=.698)
    sphere1 = Object(CoordToNP(.1, -.3, 0,),'sphere', material1, radius=.105)
    sphere2 = Object(CoordToNP(-.3, 0, 0,), 'sphere', material2, radius=.155)

    plane0 = Object(CoordToNP(0, -15_000.6, -1), 'sphere', planemat, radius=15_000)

    light0 = Object(CoordToNP(5, 5, 5), 'light', lightmat, 1, None)

    sphere_list = [sphere0, sphere1, sphere2, plane0]
    offset = 1e-05

    image = np.zeros((screen.resolution[1], screen.resolution[0], 3))
    for i, y in enumerate(np.linspace(screen.top, screen.bottom, screen.resolution[1])):
        for j, x in enumerate(np.linspace(screen.left, screen.right, screen.resolution[0])):
            pixel = ValToNP(x, y, 0)
            origin = camera.world_position
            direction = Normalize(pixel - origin)

            colour = np.zeros((3))
            refelection = 1
            for k in range(max_depth):
                #if k != 0:
                #    print(f"DEBUG_K: {(k)}")
                nearest_sphere, min_distance = Nearest_Intersected_Sphere(sphere_list, origin, direction)
                if nearest_sphere is None:
                    break

                intersection = origin + min_distance * direction
                norm_to_surface = Normalize(intersection - nearest_sphere.world_position)
                shift_point = intersection + offset * norm_to_surface
                intersection_to_light = Normalize(light0.world_position - shift_point)

                _, min_distance = Nearest_Intersected_Sphere(sphere_list, shift_point, intersection_to_light)
                intersection_to_light_distance = np.linalg.norm(light0.world_position - intersection)
                is_shadowed = min_distance < intersection_to_light_distance

                if is_shadowed:
                    break

                illumination = np.zeros((3))

                illumination += nearest_sphere.material.ambient * light0.material.ambient

                illumination += nearest_sphere.material.diffuse * light0.material.diffuse * np.dot(intersection_to_light, norm_to_surface)

                intersection_to_camera = Normalize(camera.world_position - intersection)
                H = Normalize(intersection_to_light + intersection_to_camera)
                illumination += nearest_sphere.material.specular * light0.material.specular * np.dot(norm_to_surface, H) ** (nearest_sphere.material.shininess / 4)

                colour += refelection * illumination
                refelection *= nearest_sphere.material.reflectiveness

                origin = shift_point
                direction = Reflect(direction, norm_to_surface)

            image[i, j]= np.clip(colour, 0, 1)
        print("Progress: %d/%d" % (i + 1, screen.resolution[1]))

    plt.imshow(image)
    plt.imsave(f'{(uuid5(uuid4(), "Image").hex)[:8]}.png', image)