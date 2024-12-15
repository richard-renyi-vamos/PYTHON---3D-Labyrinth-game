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

# GUI colors
GUI_WHITE = (255, 255, 255)
GUI_BLACK = (0, 0, 0)
GUI_BLUE = (0, 0, 255)


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


def draw_gui(screen, font):
    screen.fill(GUI_BLACK)
    title_text = font.render("Maze Game", True, GUI_WHITE)
    screen.blit(title_text, (20, 20))

    start_button = pygame.Rect(20, 80, 150, 50)
    quit_button = pygame.Rect(20, 150, 150, 50)

    pygame.draw.rect(screen, GUI_BLUE, start_button)
    pygame.draw.rect(screen, GUI_BLUE, quit_button)

    start_text = font.render("Start", True, GUI_WHITE)
    quit_text = font.render("Quit", True, GUI_WHITE)

    screen.blit(start_text, (45, 90))
    screen.blit(quit_text, (45, 160))

    return start_button, quit_button


def game_loop():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Maze Game")
    font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()

    running = True
    game_started = False

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN and not game_started:
                mouse_pos = pygame.mouse.get_pos()
                start_button, quit_button = draw_gui(screen, font)
                if start_button.collidepoint(mouse_pos):
                    game_started = True
                if quit_button.collidepoint(mouse_pos):
                    running = False

        if game_started:
            # Initialize OpenGL for 3D rendering
            pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
            gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
            glTranslatef(-WIDTH * CELL_SIZE, -HEIGHT * CELL_SIZE, -50)

            maze = generate_maze(WIDTH, HEIGHT)

            while game_started:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_started = False
                        running = False

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glColor3fv(WHITE)
                draw_maze(maze)

                pygame.display.flip()
                pygame.time.wait(10)

        else:
            start_button, quit_button = draw_gui(screen, font)
            pygame.display.flip()
            clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
