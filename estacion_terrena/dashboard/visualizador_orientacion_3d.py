import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Datos del giroscopio (simulados para este ejemplo)
gyro_data = [0.0, 0.0, 0.0]  # [gyro_x, gyro_y, gyro_z]

def draw_cube():
    vertices = [(1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1),
                (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), 
             (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Actualiza la rotación con los datos del giroscopio
        glRotatef(gyro_data[0], 1, 0, 0)  # Rotación en X
        glRotatef(gyro_data[1], 0, 1, 0)  # Rotación en Y
        glRotatef(gyro_data[2], 0, 0, 1)  # Rotación en Z

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
    