import time as t
import glm
from functools import lru_cache as lcache
import threading as thr
from concurrent.futures import ThreadPoolExecutor as ThrPoolEx
import sys
import os

#constants
SQPI = 9.869604401089358618834490999876151
GRAVITY = 9.81 # m * 1/s^2
SUN_COLOR = glm.vec3(0.99609375, 0.83203125, 0.5390625) #RGB01
EIGENGRAU_COLOR = glm.vec3(0.0859375, 0.0859375, 0.11328125) #RGB01
OFFSET = 1e-6
π = glm.pi()

#variables
ø = ''

#classes
class Screen:
    __slots__ = ('resolution', 'x', 'y', 'aspect_ratio', 'ar')

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

    def __init__(self, R:float, G:float, B:float, transparency:float, metallicity:float, roughness:float, specular:float) -> None:
        self.color = glm.vec3(R, G, B)
        self.transparency = transparency
        self.metallicity = metallicity
        self.roughness = roughness
        self.specular = specular

class Light:

    def __init__(self, world_position:glm.vec3, R:float=SUN_COLOR.x, G:float=SUN_COLOR.y, B:float=SUN_COLOR.z, is_point:bool = True) -> None:
        self.world_position = world_position
        self.color = glm.vec3(R, G, B)
        self.is_point = is_point

class Sphere:

    def __init__(self) -> None:
        pass
    
class Triangle:

    def __init__(self) -> None:
        pass

class Program:
    def __init__(self, screen:Screen, camera:Camera) -> None:
        self.screen = screen
        self.camera = camera
        self.should_run = True

    @lcache(24)
    def ReturnBaseArray(self, x:float, y:float, z:float) -> glm.array:
        return glm.array(*((glm.vec3(x, y, z),) * (self.screen.x * self.screen.y)))

    def Render(self):
        while self.should_run:
            t0 = t.time()

            screen = self.ReturnBaseArray(EIGENGRAU_COLOR.x, EIGENGRAU_COLOR.y, EIGENGRAU_COLOR.z)
            for y in range(self.screen.y//2, (self.screen.y//-2) - 1, -1):
                #-1 * self.camera.fov / self.screen.aspect_ratio, self.camera.fov / self.screen.aspect_ratio, (self.camera.half_fov / self.screen.aspect_ratio) / self.screen.y
                for x in range(self.screen.x//-2, (self.screen.x//2) + 1, +1):
                    #-1 * self.camera.fov, self.camera.fov + OFFSET, self.camera.half_fov/self.screen.x
                    pass


            t1 = t.time()
            print(f'{1/(t1-t0):.3f}')
    
#functions
def Normalize(vector):
    return vector / glm.lenght(vector)

def MakeSphereList(*spheres) -> list:
    return list(*spheres)

if __name__ == '__main__':
    game = Program(Screen(1088, 680), Camera(glm.dvec3(0.0, 1.0, 0.0), 60.0, OFFSET, 2000))
    game.Render()
    sys.exit()