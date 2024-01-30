import numba
import numpy as np
import matplotlib.pyplot as plt
from uuid import uuid4
from numpy import ndarray
from functools import lru_cache

sqpi = 9.869604401089358

@numba.njit(fastmath=True)
def Clamp(x:float, mi_ma:tuple[float, float]= (0, 1)) -> float:
    return x * (mi_ma[0] < x) * (mi_ma[1] > x) + mi_ma[0] * (mi_ma[0] >= x) + mi_ma[1] * (mi_ma[1] <= x)

@lru_cache(2048)
def ToNP(x:float, y:float, z:float) -> ndarray:
    return np.array([x, y, z])

@numba.njit(fastmath=True, cache=True)
def Normalize(vector:ndarray) -> ndarray:
    return vector / np.linalg.norm(vector)

@numba.njit(fastmath=True, cache=True)
def Reflect(vector:ndarray, axis:ndarray) -> ndarray:
    return vector - 2 * np.dot(vector, axis) * axis

# @numba.njit(fastmath=True)
# def c255to1(x:int) -> float:
#     x:float = Clamp(x, (0, 255))
#     return x/255

@numba.njit(fastmath=True)
def M_Square(x:float) -> float:
    return x * x

# @numba.njit(fastmath=True)
# def M_Cube(x:float) -> float:
#     return x * x * x

@numba.njit(fastmath=True, cache=True)
def Sphere_Intersect(position:ndarray, radius:float, ray_origin:ndarray, ray_direction:ndarray) -> float | None:
    b = 2 * np.dot(ray_direction, ray_origin - position)
    c = M_Square(np.linalg.norm(ray_origin - position)) - M_Square(radius)
    delta = b ** 2 - 4 * c
    if delta >= 0:
        t1:float = (-b + np.sqrt(delta)) / 2
        t2:float = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None

def Nearest_Intersected_Sphere(sphere_list:list, ray_origin:ndarray, ray_direction:ndarray) -> tuple[None, float]:
    distances = [Sphere_Intersect(sphere.world_position, sphere.radius, ray_origin, ray_direction)for sphere in sphere_list]
    nearest_sphere = None
    min_dist = np.inf
    for ind, dist in enumerate(distances):
        if dist and dist < min_dist:
            min_dist = dist
            nearest_sphere = sphere_list[ind]
    return nearest_sphere, min_dist

# def Divide_Res(cores: int, y: int) -> list:
#     r = int(y % cores)
#     p = int((y - r) / cores)
#     o = 0
#     lst = []
    
#     if r == 0:
#         for i in range(o, y, p):
#             o += 1
#             lst.append([i + 1, o * p])
#     else:
#         for i in range(o, y - p, p):
#             o += 1
#             if r > 0:
#                 r -= 1
#                 try:
#                     lst.append([last + 1, last + 1 + p])
#                     last += 1 + p
#                 except Exception:
#                     lst.append([i+1, o * p + 1])
#                     last = o * p + 1
#             else:
#                 try:
#                     lst.append([last + 1, last + p])
#                     last += p
#                 except Exception:
#                     lst.append([i + 1, o * p + 1])
#                     last = o * p + 1
#     return lst

class Material():
    __slots__ = ("ambient", "diffuse", "specular", "shininess", "reflectiveness")

    def __init__(self, ambient:ndarray, diffuse:ndarray, specular:ndarray, shininess:float, reflectiveness:float) -> None:
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        try:
            self.reflectiveness = M_Square(Clamp(reflectiveness))
        except:
            self.reflectiveness = None
            
class Object():
    __slots__ = ("world_position", "tpe", "material", "light_intensity", "radius")

    def __init__(self, world_positiom:ndarray, tpe:str, material:Material, light_intensity:float = 0, radius:float = None) -> None:
        tpe = tpe.lower()
        self.world_position = world_positiom
        self.tpe = tpe
        self.material = material
        if tpe == 'light':
            self.light_intensity = light_intensity
        elif tpe == 'sphere':
            self.radius = radius

class Screen():
    __slots__ = ("resolution", "aspect_ratio", "left", "right", "top", "bottom", "x", "y")
    def __init__(self, x:int, y:int) -> None:
        self.resolution = self.x, self.y = x, y
        self.aspect_ratio = float(x)/y
        self.left = -1.0
        self.right = 1.0
        self.top = 1.0 / (float(x)/y)
        self.bottom = -1.0 / (float(x)/y)


class Camera():
    __slots__ = 'world_position', 'fov', 'far', 'near'

    def __init__(self, world_position:ndarray, fov:float, near:float, far:int) -> None:
        self.world_position = world_position
        self.fov = fov
        self.near = near
        self.far = float(far)

def Render():
    screen = Screen(1088, 680)
    camera = Camera(ToNP(0, 0, 2), 60, 0.01, 32_000)

    max_depth = 8

    material0 = Material(ToNP(.18, 0, 0), ToNP(.7, 0, 0), ToNP(1, 1, 1), 100., .5)
    material1 = Material(ToNP(.1, 0, 0.1), ToNP(.7, 0, .7), ToNP(1, 1, 1), 100., .3)
    material2 = Material(ToNP(0, 0.123, 0), ToNP(0, 0.6, 0), ToNP(1, 1, 1), 100., .7)
    lightmat = Material(ToNP(1, 1, 1), ToNP(1, 1, 1), ToNP(1, 1, 1), 100, 1)
    planemat = Material(ToNP(0.189, 0.202, 0.21), ToNP(0.4, 0.4, 0.4), ToNP(.5, .5, .5), 100, 1)
    sphere0 = Object(ToNP(-2.0, 0, -1), 'sphere', material0, radius=.698)
    sphere1 = Object(ToNP(.1, -.3, 0,),'sphere', material1, radius=.105)
    sphere2 = Object(ToNP(-.3, 0, 0,), 'sphere', material2, radius=.155)

    plane0 = Object(ToNP(0, -15_001., -1), 'sphere', planemat, radius=15_000)

    light0 = Object(ToNP(4, 6, 5), 'light', lightmat, 1, None)

    sphere_list = [sphere0, sphere1, sphere2, plane0]
    offset = 1e-05

    image = np.zeros((screen.y, screen.x, 3))
    for i, y in enumerate(np.linspace(screen.top, screen.bottom, screen.y)):
        for j, x in enumerate(np.linspace(screen.left, screen.right, screen.x)):
            pixel = ToNP(x, y, 0)
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
    plt.imsave(f'{uuid4().hex[:8]}.png', image)