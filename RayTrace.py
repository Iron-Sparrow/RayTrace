import numpy as np
import time 
import matplotlib.pyplot as plt
from uuid import uuid5, uuid4

def Convert255to1(x:int) -> float:
    if x not in range(0, 255):
        raise ValueError(f"Input not valid (0-255), {x}")
    return float(x)/255

def M_Square(x:float) -> float:
    return (x*x)

def M_Cube(x:float) -> float:
    return(x*x*x)

def ToNP(x, y, z):
    return np.array([x,y,z])

def Normalize(vector):
    return vector / np.linalg.norm(vector)

def Reflect(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def Sphere_Intersect(position, radius, ray_origin, ray_direction):
    a = 1.0
    b = 2 * np.dot(ray_direction, ray_origin - position)
    c = np.linalg.norm(ray_origin - position) ** 2 - radius ** 2
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / (2*a)
        t2 = (-b - np.sqrt(delta)) / (2*a)
        if t1 > 0 and t2 > 0:
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
    def __init__(self, ambient:np.ndarray, diffuse:np.ndarray, specular:np.ndarray, shininess:float, reflectiveness:float):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflectiveness = reflectiveness
        
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
    def __init__(self, x:int, y:int):
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


def Main():            
    screen = Screen(400, 250)
    camera = Camera(0, 0, 1, 60.0, 0.01, 32_000)

    max_depth = 8

    material0 = Material(ToNP(Convert255to1(45), 0, 0), ToNP(.7, 0, 0), ToNP(1, 1, 1), 100, M_Square(.5))
    material1 = Material(ToNP(0.1, 0, 0.1), ToNP(.7, 0, 0.7), ToNP(1, 1, 1), 100, M_Square(.3))
    material2 = Material(ToNP(0, 0.1, 0), ToNP(0, 0.6, 0), ToNP(1, 1, 1), 100, M_Square(.7))
    lightmat = Material(ToNP(1, 1, 1), ToNP(1, 1, 1), ToNP(1, 1, 1), None, None)
    planemat = Material(ToNP(0.1, 0.1, 0.1), ToNP(.6, .6, .6), ToNP(1, 1, 1), 100, 1)

    sphere0 = Object("Sphere0", -2.0, 0, -1, False, 'sphere', material0,.7)
    sphere1 = Object("Sphere1", .1, -.3, 0, False, 'sphere', material1, .1)
    sphere2 = Object("Sphere2", -.3, 0, 0, False, 'sphere', material2, .15)

    plane0 = Object("Plane", 0, -15_001, -1, False, 'sphere', planemat, 15_000)

    light0 = Object("Light0", 5, 5, 5, True, 'light', lightmat)

    sphere_list = [sphere0, sphere1, sphere2, plane0]
    offset = 1e-05

    image = np.zeros((screen.resolution[1], screen.resolution[0], 3))
    for i, y in enumerate(np.linspace(screen.top, screen.bottom, screen.resolution[1])):
        for j, x in enumerate(np.linspace(screen.left, screen.right, screen.resolution[0])):
            pixel = ToNP(x, y, 0)
            origin = camera.world_position
            direction = Normalize(pixel - origin)

            colour = np.zeros((3))
            refelection = 1
            for k in range(max_depth):
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


if __name__ == '__main__':
    ot = time.time()
    Main()
    print(f"{((time.time() - ot) * 1000):.2f} ms, {(time.time() - ot):.3f} s, {(1/(time.time() - ot)):.3f} Hz")