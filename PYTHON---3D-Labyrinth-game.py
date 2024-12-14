import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Maze parameters
WIDTH = 20
HEIGHT = 20
CELL_SIZE = 2

# Colors
WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
RED = (1, 0, 0)

def generate_maze(width, height):
    maze = [[1 for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width * 2 and 0 < ny < height * 2 and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    return maze

def draw_maze(maze):
    glBegin(GL_QUADS)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                glVertex3f(x * CELL_SIZE, y * CELL_SIZE, 0)
                glVertex3f((x + 1) * CELL_SIZE, y * CELL_SIZE, 0)
                glVertex3f((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, 0)
                glVertex3f(x * CELL_SIZE, (y + 1) * CELL_SIZE, 0)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
    glTranslatef(-WIDTH * CELL_SIZE, -HEIGHT * CELL_SIZE, -50) # Adjust camera position

    maze = generate_maze(WIDTH, HEIGHT)

    player_x = 1 * CELL_SIZE
    player_y = 1 * CELL_SIZE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-1, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(1, 0, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, 1, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3fv(WHITE)
        draw_maze(maze)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
