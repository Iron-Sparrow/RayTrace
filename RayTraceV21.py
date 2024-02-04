import time as t
import glm
from functools import cache
import threading as thr
from concurrent.futures import ThreadPoolExecutor as ThrPoolEx
import sys

#constants
SQPI = 9.869604401089358618834490999876151
GRAVITY = 9.81 # m * 1/s^2
ARTISTIC_SUN_COLOR = glm.vec3(0.99609375, 0.83203125, 0.5390625) #RGB01
SUN_COLOR = glm.vec3(0.99609375, 0.8828125, 0.7890625) #RGB01
EIGENGRAU_COLOR = glm.vec3(0.0859375, 0.0859375, 0.11328125) #RGB01
NATURAL_LIGHT_COLOR = glm.vec3(0.99609375, 0.8046875, 0.6484375) #RGB01
OFFSET = 1e-6
π = glm.pi() # pi

#variables
ø = '' #empty string

#classes
class Screen:
    __slots__ = ('resolution', 'x', 'y', 'aspect_ratio', 'ar',)

    def __init__(self, width:int, height:int) -> None:
        self.resolution = glm.u16vec2(width, height)
        self.x = self.resolution.x
        self.y = self.resolution.y
        self.aspect_ratio = float(self.x) / self.y
        self.ar = self.aspect_ratio

class Camera:
    __slots__ = ('world_position', 'wp', 'field_of_view', 'fov', 'far', 'near', 'half_fov', 'view_depth')

    def __init__(self, world_position:glm.dvec3, field_of_view:float, near:float, far:int) -> None:
        self.wp = self.world_position = world_position
        
        self.field_of_view = field_of_view
        self.fov = self.field_of_view
        self.far = float(far)
        self.near = near
        self.half_fov = field_of_view / 2
        self.view_depth = float(far) - near

class Material:
    __slots__ = ('color', 'transparency', 'metallicity', 'roughness', 'specular')

    def __init__(self, R:float, G:float, B:float, transparency:float, roughness:float, metallicity:float, specular:float) -> None:
        self.color = glm.vec3(R, G, B)
        self.transparency = transparency
        self.metallicity = metallicity
        self.roughness = roughness
        self.specular = specular

class Light:
    __slots__ = ('world_position', 'color', 'is_point',)

    def __init__(self, world_position:glm.dvec3, R:float=NATURAL_LIGHT_COLOR.x, G:float=NATURAL_LIGHT_COLOR.y, B:float=NATURAL_LIGHT_COLOR.z, is_point:bool = True) -> None:
        self.world_position = world_position
        self.color = glm.vec3(R, G, B)
        self.is_point = is_point

class DirectionalLight:
    __slots__ = 'direction', 'color', 

    def __init__(self, direction, R:float=SUN_COLOR.x, G:float=SUN_COLOR.y, B:float=SUN_COLOR.z) -> None:
        self.direction = direction
        self.color = glm.vec3(R, G, B)

class Sphere:

    def __init__(self, world_position:glm.vec3, radius:float, material:Material) -> None:
        self.world_position = world_position
        self.radius = radius
        self.material = material
    
class Triangle:

    def __init__(self) -> None:
        pass

class Program:
    def __init__(self, screen:Screen, camera:Camera, automatically_get_performance_by_reducing_beauty:bool, target_fps:int|None = None) -> None:
        self.screen = screen
        self.camera = camera
        self.should_run = True
        self.auto_balance_opti = automatically_get_performance_by_reducing_beauty
        self.target_fps = 30 if not target_fps else target_fps

    @cache
    def ReturnBaseArray(self, x:float, y:float, z:float) -> glm.array:
        return glm.array(*((glm.vec3(x, y, z),) * (self.screen.x * self.screen.y)))
    
    @cache
    def ReturnPixelVec3(self, x:int, y:int) -> glm.dvec3:
        return glm.dvec3(x, y, 0)
    
    @cache
    def Sphere_Intersect(self, world_position:glm.vec3, radius:float, ray_origin:glm.vec3, ray_direction:glm.vec3) -> float|None:
        b = 2 * glm.dot(ray_direction, ray_origin - world_position)
        c = glm.length2(ray_origin - world_position) - glm.pow(radius, 2) #type:ignore
        delta = glm.pow(b, 2) - 4 * c
        if delta > 0:
            t1 = (-b - glm.sqrt(delta)) / 2
            t2 = (-b + glm.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                return glm.min(t1, t2)
        return None
    
    @cache
    def Nearest_Intersected_Sphere(self, ray_origin:glm.vec3, ray_direction:glm.vec3, *sphere_list:list):
        distances = [self.Sphere_Intersect(sphere.world_position, sphere.radius, ray_origin, ray_direction) for sphere in sphere_list]
        nearest_sphere = None
        min_dist = self.camera.far
        for index, distance in enumerate(distances):
            if distance and distance < min_dist:
                min_dist = distance
                # nearest_sphere

    def Render(self, max_bounce):
        max_bounce = glm.clamp(max_bounce, 1, 32)

        while self.should_run:
            t0 = t.time()

            screen = self.ReturnBaseArray(EIGENGRAU_COLOR.x, EIGENGRAU_COLOR.y, EIGENGRAU_COLOR.z)
            for y in range(self.screen.y//2, (self.screen.y//-2) - 1, -1):
                #-1 * self.camera.fov / self.screen.aspect_ratio, self.camera.fov / self.screen.aspect_ratio, (self.camera.half_fov / self.screen.aspect_ratio) / self.screen.y
                for x in range(self.screen.x//-2, (self.screen.x//2) + 1, +1):
                    #-1 * self.camera.fov, self.camera.fov + OFFSET, self.camera.half_fov/self.screen.x
                    pixel = self.ReturnPixelVec3(x, y)
                    origin = self.camera.world_position

                    direction = Normalize(pixel - origin) #type:ignore

                    pixel_color = glm.vec3(0.0, 0.0, 0.0)
                    reflection_intensity = 1.0

                    for _dis in range(max_bounce): #discard
                        ...

            t1 = t.time()
            t_elapse = t1 - t0
            fps = 1./t_elapse
            if self.auto_balance_opti:
                if fps < self.target_fps:
                    if max_bounce > 2:
                        max_bounce -= 1
                elif fps > 2 * self.target_fps - fps:
                    if max_bounce < 32:
                        max_bounce += 2


            print(f'{1/(t_elapse):.3f}, {max_bounce}')
    
#functions
@cache
def Normalize(vector):
    return vector / glm.length(vector)

def MakeSphereList(*spheres) -> list:
    return list(*spheres)

if __name__ == '__main__':
    screen = Screen(320, 180)
    camera = Camera(glm.dvec3(0.0, 1.6, 1.0), 40, OFFSET, 2000)
    game = Program(screen, camera, True, 30)
    game.Render(8) #max depth is in between 1 and 32
    sys.exit()