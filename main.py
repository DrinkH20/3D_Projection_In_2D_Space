import pygame
import math
import random

plot_cube_place = []
plot_points = []
block_type = []

run = True
angleX = 0
angleY = 1
angleZ = 0
rotated = []
rotated_points = []
Y = 0
level_size = 9

X = 0
Z = 0

origin = [0, 0, 0]

scrn_w = 500
scrn_h = 500

grass = (100, 200, 100)
rock = (100, 100, 100)
wood = (150, 150, 100)



distance = 2
cam_x = 300
cam_y = 250

repeat = 0

window = pygame.display.set_mode((scrn_w, scrn_h))


def generate_level():
    for y in range(level_size - 2):
        for x in range(level_size):
            for z in range(level_size):
                plot_cube_place.append((x * 2, y * 2 + 4, z * 2))
                block_type.append(rock)
    for y in range(1):
        for x in range(level_size):
            for z in range(level_size):
                plot_cube_place.append((x * 2, y * 2 + 2, z * 2))
                block_type.append(wood)
    for y in range(1):
        for x in range(level_size):
            for z in range(level_size):
                plot_cube_place.append((x * 2, y * 2, z * 2))
                block_type.append(grass)
                if random.randint(1, 20) == 1:
                    generate_tree(x, y, z)


def append(list, item, m1, m2, m3):
    a = item[0] + m1
    b = item[1] + m2
    c = item[2] + m3
    thing = (a, b, c)
    list.append(thing)


def draw_line(p1, p2):
    if p1[0]+cam_x < scrn_w and p1[0]+cam_x > 0 and p1[1]+cam_y < scrn_h and p1[1]+cam_y > 0:
        if p2[0]+cam_x < scrn_w and p2[0]+cam_x > 0 and p2[1]+cam_y < scrn_h and p2[1]+cam_y > 0:
            pygame.draw.line(window, color, (p1[0]+cam_x, p1[1]+cam_y), (p2[0]+cam_x, p2[1]+cam_y), math.floor(z*5))

def generate_tree(x, y, z):
    plot_cube_place.append((x * 2, y * 2 - 2, z * 2))
    block_type.append(wood)
    plot_cube_place.append((x * 2, y * 2 - 4, z * 2))
    block_type.append(wood)
    plot_cube_place.append((x * 2 - 2, y * 2 - 6, z * 2))
    block_type.append(grass)
    plot_cube_place.append((x * 2 + 2, y * 2 - 6, z * 2))
    block_type.append(grass)
    plot_cube_place.append((x * 2, y * 2 - 6, z * 2 - 2))
    block_type.append(grass)
    plot_cube_place.append((x * 2, y * 2 - 6, z * 2 + 2))
    block_type.append(grass)
    plot_cube_place.append((x * 2, y * 2 - 8, z * 2))
    block_type.append(grass)


def rotatex(x, y, z):
    global X
    global Y
    global Z
    X = x
    Y = (y + origin[1])*math.cos(angleX) - (z + origin[2])*math.sin(angleX)
    Z = (y + origin[1])*math.sin(angleX) + (z + origin[2])*math.cos(angleX)
    return X, Y, Z


def rotatey(x, y, z):
    global X
    global Y
    global Z
    X = (x + origin[0])*math.cos(angleY) - (z + origin[2])*math.sin(angleY)
    Y = y
    Z = (x + origin[0])*math.sin(angleY) + (z + origin[2])*math.cos(angleY)
    return X, Y, Z


def rotatez(x, y, z):
    global X
    global Y
    global Z
    X = (x + origin[0])*math.cos(angleZ) - (y + origin[1])*math.sin(angleZ)
    Y = (x + origin[0])*math.sin(angleZ) + (y + origin[1])*math.cos(angleZ)
    Z = z
    return X, Y, Z


generate_level()

while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(30)
    window.fill((0, 0, 20))

    plot_points = []
    for i in plot_cube_place:
        append(plot_points, i, 1, 1, -1)
        append(plot_points, i, -1, 1, -1)
        append(plot_points, i, -1, -1, -1)
        append(plot_points, i, 1, -1, -1)
        append(plot_points, i, 1, 1, 1)
        append(plot_points, i, -1, 1, 1)
        append(plot_points, i, -1, -1, 1)
        append(plot_points, i, 1, -1, 1)

    rotated_points = []
    for i in plot_points:
        rotated = i
        X = 0
        Y = 0
        Z = 0
        rotated = rotatez(rotated[0], rotated[1], rotated[2])
        rotated = rotatex(rotated[0], rotated[1], rotated[2])
        rotated = rotatey(rotated[0], rotated[1], rotated[2])
        # z = 1 / (distance * 2 - rotated[2])
        z = 300 / (300 + rotated[2] * 10)
        rotated_points.append((rotated[0] * 25 * z, rotated[1] * 25 * z, z))
        # rotated_points.append((rotated[0] * 25, rotated[1] * 25, z))

    repeat = 0
    color = block_type[0]
    while repeat < len(rotated_points):
        if repeat != 0:
            color = block_type[int(repeat / 8)]
        draw_line(rotated_points[repeat + 0], rotated_points[repeat + 1])
        draw_line(rotated_points[repeat + 1], rotated_points[repeat + 2])
        draw_line(rotated_points[repeat + 2], rotated_points[repeat + 3])
        draw_line(rotated_points[repeat + 3], rotated_points[repeat + 0])
        draw_line(rotated_points[repeat + 4], rotated_points[repeat + 5])
        draw_line(rotated_points[repeat + 5], rotated_points[repeat + 6])
        draw_line(rotated_points[repeat + 6], rotated_points[repeat + 7])
        draw_line(rotated_points[repeat + 7], rotated_points[repeat + 4])
        draw_line(rotated_points[repeat + 4], rotated_points[repeat + 0])
        draw_line(rotated_points[repeat + 5], rotated_points[repeat + 1])
        draw_line(rotated_points[repeat + 6], rotated_points[repeat + 2])
        draw_line(rotated_points[repeat + 7], rotated_points[repeat + 3])
        repeat += 8

    if keys[pygame.K_a]:
        origin[0] += -.5
    if keys[pygame.K_d]:
        origin[0] += .5
    if keys[pygame.K_w]:
        origin[1] += .5
    if keys[pygame.K_s]:
        origin[1] += -.5

    if keys[pygame.K_RIGHT]:
        angleY += -.05
    if keys[pygame.K_LEFT]:
        angleY += .05

    if keys[pygame.K_UP]:
        angleX += .05
    if keys[pygame.K_DOWN]:
        angleX += -.05

    if keys[pygame.K_z]:
        angleZ += .05
    if keys[pygame.K_x]:
        angleZ += -.05
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
