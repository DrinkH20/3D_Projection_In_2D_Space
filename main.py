import pygame
import math
import random
from sorting import quicksort

plot_cube_place = []
plot_points = []
block_type = []
lines = []

run = True
angleX = 0
angleY = 1.6
angleZ = 0
rotated = []
rotated_points = []
Y = 0
level_w = 6
level_h = 3
level_d = 6

forward_v = 0
side_v = 0

X = 0
Z = 0

scrn_w = 500
scrn_h = 500

grass = (100, 200, 100)
rock = (100, 100, 100)
wood = (150, 150, 100)
player = (100, 100, 200)

origin = (0, 0, 10)
past_origin = (origin[0], origin[1], origin[2], player)

distance = 2
cam_x = 250
cam_y = 300

repeat = 0

zoom = 300

window = pygame.display.set_mode((scrn_w, scrn_h))

plot_cube_place.append((origin[0], origin[1], origin[2], player))


def generate_level():
    for y in range(level_h - 2):
        for x in range(level_w):
            for depth in range(level_d):
                plot_cube_place.append((x * 2, y * 2 + 4, depth * 2, rock))
    for y in range(1):
        for x in range(level_w):
            for depth in range(level_d):
                plot_cube_place.append((x * 2, y * 2 + 2, depth * 2, wood))
    for y in range(1):
        for x in range(level_w):
            for depth in range(level_d):
                plot_cube_place.append((x * 2, y * 2, depth * 2, grass))
                if random.randint(1, 20) == 1:
                    generate_tree(x, y, depth)


def append(lst, item, m1, m2, m3):
    a = item[0] + m1
    b = item[1] + m2
    c = item[2] + m3
    thing = (a, b, c)
    lst.append(thing)


def draw_line(p1, p2):
    if (p1[0]+cam_x < scrn_w) and (p1[0]+cam_x > 0) and (p1[1]+cam_y < scrn_h) and (p1[1]+cam_y > 0):
        if (p2[0]+cam_x < scrn_w) and (p2[0]+cam_x > 0) and (p2[1]+cam_y < scrn_h) and (p2[1]+cam_y > 0):
            if p1[2] + p2[2] * 3 > 1.5:
                if int(p1[2] + p2[2]) < 30:
                    line_size = p1[2] + p2[2]
                else:
                    line_size = 20
                pygame.draw.line(window, color, (p1[0]+cam_x, p1[1]+cam_y),
                                 (p2[0]+cam_x, p2[1]+cam_y), int(line_size * 3))


def generate_tree(x, y, gz):
    plot_cube_place.append((x * 2, y * 2 - 2, gz * 2, wood))
    plot_cube_place.append((x * 2, y * 2 - 4, gz * 2, wood))
    plot_cube_place.append((x * 2 - 2, y * 2 - 6, gz * 2, grass))
    plot_cube_place.append((x * 2 + 2, y * 2 - 6, gz * 2, grass))
    plot_cube_place.append((x * 2, y * 2 - 6, gz * 2 - 2, grass))
    plot_cube_place.append((x * 2, y * 2 - 6, gz * 2 + 2, grass))
    plot_cube_place.append((x * 2, y * 2 - 8, gz * 2, grass))


def rotate_x(x, y, z):
    global X
    global Y
    global Z
    X = x
    Y = y*math.cos(angleX) - z*math.sin(angleX)
    Z = y*math.sin(angleX) + z*math.cos(angleX)
    return X, Y, Z


def rotate_y(x, y, z):
    global X
    global Y
    global Z
    X = x*math.cos(angleY) - z*math.sin(angleY)
    Y = y
    Z = x*math.sin(angleY) + z*math.cos(angleY)
    return X, Y, Z


def rotate_z(x, y, z):
    global X
    global Y
    global Z
    X = x*math.cos(angleZ) - y*math.sin(angleZ)
    Y = x*math.sin(angleZ) + y*math.cos(angleZ)
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
        rotated = rotate_z(rotated[0] - origin[0], rotated[1] - origin[1], rotated[2] - origin[2])
        rotated = rotate_x(rotated[0], rotated[1], rotated[2])
        rotated = rotate_y(rotated[0], rotated[1], rotated[2])
        z = zoom / (zoom + rotated[2] * 10)
        rotated_points.append((rotated[0] * 25 * z, rotated[1] * 25 * z, z))
    repeat = 0
    lines = []
    while repeat < len(rotated_points):
        per = plot_cube_place[int(repeat/8)]
        color = per[3]

        lines.append((rotated_points[repeat + 0], rotated_points[repeat + 1], color))
        lines.append((rotated_points[repeat + 1], rotated_points[repeat + 2], color))
        lines.append((rotated_points[repeat + 2], rotated_points[repeat + 3], color))
        lines.append((rotated_points[repeat + 3], rotated_points[repeat + 0], color))
        lines.append((rotated_points[repeat + 4], rotated_points[repeat + 5], color))
        lines.append((rotated_points[repeat + 5], rotated_points[repeat + 6], color))
        lines.append((rotated_points[repeat + 6], rotated_points[repeat + 7], color))
        lines.append((rotated_points[repeat + 7], rotated_points[repeat + 4], color))
        lines.append((rotated_points[repeat + 4], rotated_points[repeat + 0], color))
        lines.append((rotated_points[repeat + 5], rotated_points[repeat + 1], color))
        lines.append((rotated_points[repeat + 6], rotated_points[repeat + 2], color))
        lines.append((rotated_points[repeat + 7], rotated_points[repeat + 3], color))
        repeat += 8

    s = 0
    e = len(lines) - 1
    lines = quicksort(lines, s, e, 2)

    repeat = 0
    for i in lines:
        if repeat/12 == round(repeat/12):
            per = plot_cube_place[int(repeat / 12)]
        color = i[2]
        draw_line(i[0], i[1])
        repeat += 1

    origin = list(origin)

    forward_v = (forward_v * .8)

    if keys[pygame.K_w]:
        forward_v -= .2
    if keys[pygame.K_s]:
        forward_v += .2

    origin[2] -= math.cos(angleY) * forward_v
    origin[0] -= math.sin(angleY) * forward_v

    side_v = (side_v * .8)

    if keys[pygame.K_d]:
        side_v -= .2
    if keys[pygame.K_a]:
        side_v += .2

    origin[2] += math.sin(angleY) * side_v
    origin[0] -= math.cos(angleY) * side_v

    if keys[pygame.K_q]:
        origin[1] += -.5
    if keys[pygame.K_e]:
        origin[1] += .5

    origin = tuple(origin)

    if keys[pygame.K_RIGHT]:
        angleY += math.cos(angleZ) * .05
        angleX += math.sin(angleZ) * .05
        angleZ -= math.sin(angleX) * .05

    if keys[pygame.K_LEFT]:
        angleY -= math.cos(angleZ) * .05
        angleX -= math.sin(angleZ) * .05
        angleZ += math.sin(angleX) * .05

    if keys[pygame.K_UP]:
        angleZ -= math.sin(angleY) * .05
        angleX += math.cos(angleY) * .05
    if keys[pygame.K_DOWN]:
        angleZ += math.sin(angleY) * .05
        angleX -= math.cos(angleY) * .05

    if keys[pygame.K_z]:
        angleX += .05
    if keys[pygame.K_x]:
        angleX += -.05

    if keys[pygame.K_y]:
        zoom += 10
    if keys[pygame.K_h]:
        zoom += -10

    plot_cube_place[0] = (origin[0], origin[1], origin[2], player)
    past_origin = (origin[0], origin[1], origin[2], player)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
