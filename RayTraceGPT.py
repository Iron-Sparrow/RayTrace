import glm
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

class Light:
    def __init__(self, position, color):
        self.position = position
        self.color = color

spheres = [Sphere(glm.vec3(0, 0, -5), 1, glm.vec3(1, 0, 0)),
           Sphere(glm.vec3(2, 0, -5), 1, glm.vec3(0, 1, 0))]
lights = [Light(glm.vec3(-2, 2, 0), glm.vec3(1, 1, 1))]

def intersect(ray_origin, ray_direction, sphere):
    oc = ray_origin - sphere.center
    a = np.dot(ray_direction, ray_direction)
    b = 2.0 * np.dot(oc, ray_direction)
    c = np.dot(oc, oc) - sphere.radius * sphere.radius
    discriminant = b * b - 4 * a * c

    if discriminant > 0:
        t = (-b - np.sqrt(discriminant)) / (2 * a)
        if t > 0:
            hit_point = ray_origin + t * ray_direction
            normal = glm.normalize(hit_point - sphere.center)
            return True, hit_point, normal, sphere.color

    return False, None, None, None

def trace_ray(ray_origin, ray_direction, depth=0):
    if depth > 5:
        return glm.vec3(0, 0, 0)

    closest_t = float('inf')
    closest_sphere = None

    for sphere in spheres:
        hit, _, _, _ = intersect(ray_origin, ray_direction, sphere)
        if hit:
            return sphere.color

    return glm.vec3(0, 0, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    total_pixels = 800 * 800
    processed_pixels = 0

    for i in range(800):
        for j in range(800):
            ray_direction = glm.vec3(i - 400, j - 400, -800)
            ray_direction = glm.normalize(ray_direction)
            color = trace_ray(glm.vec3(0, 0, 0), ray_direction)
            glColor3f(color.x, color.y, color.z)
            glBegin(GL_POINTS)
            glVertex2f(i, j)
            glEnd()

            processed_pixels += 1
            progress = processed_pixels / total_pixels
            if processed_pixels % 100 == 0:
                glutSwapBuffers()
                glutPostRedisplay()
                print(f"Progress: {progress * 100:.2f}%", end='\r')

    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, 800, 0, 800)

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow("Raytracer")

    init()

    glutDisplayFunc(display)
    glutMainLoop()
