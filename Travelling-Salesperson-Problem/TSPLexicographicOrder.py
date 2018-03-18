# -----------------------------------------------------------------------------
#
# TSP Using Lexicographic Order
#
# Language - Python
# Modules - pygame, sys, random, copy, math
# By - Jatin Kumar Mandav
#
# Website - https://jatinmandav.wordpress.com
#
# YouTube Channel - https://www.youtube.com/mandav
# GitHub - github.com/jatinmandav
# Twitter - @jatinmandav
#
# -----------------------------------------------------------------------------

import pygame
import sys
import random
import copy
import math

pygame.init()

width = 800
height = 450

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("TSP Lexicographical Order")


background = (50, 50, 50)
white = (236, 240, 241)
violet = (136, 78, 160)
purple = (99, 57, 116)

points = 10
d = 10

bestEverOrder = []
bestDistance = 0
order = []
count = 0.0
x = -1
pause = False


class Cities:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def reset():
    global bestEverOrder, bestDistance, order, x, count, pause
    count = 0.0
    order = []
    x = -1
    bestEverOrder = []
    bestDistance = 0
    pause = False


def main_loop():
    loop = True
    cities = []
    global bestEverOrder, bestDistance, order, x, count, pause, points
    reset()

    font = pygame.font.SysFont("Times New Roman", 20)

##    for i in range(points):
##        order.append(i)
##        x = random.randrange(10, width/2-10)
##        y = random.randrange(40, height-10)
##        i = Cities(x, y)
##        cities.append(i)

    pointsF = open("points.txt", "r")
    data = pointsF.readlines()
    pointsF.close()
    points = len(data)
    for i in range(len(data)):
        data[i] = data[i].split(" ")
        data[i][0] = int(data[i][0])
        data[i][1] = int(data[i][1])

    for i in range(len(data)):
        order.append(i)
        i = Cities(data[i][0], data[i][1])
        cities.append(i)

    bestDistance = total_distance(cities)
    bestEverOrder = copy.deepcopy(order)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main_loop()

        display.fill(background)

        dist = total_distance(cities)

        if dist < bestDistance:
            bestDistance = dist
            bestEverOrder = copy.deepcopy(order)

        next_order()
        draw(cities)

        currenttext = font.render("Current Distance : " + str(dist), True, white)
        display.blit(currenttext, (50, height - 30))

        text = font.render("Shortest Distance so Far : " + str(bestDistance), True, white)
        display.blit(text, (width / 2, height - 30))

        pygame.display.update()

        if x == -1:
            pause = True
            pauseUnpause()

        clock.tick(60)


def draw(cities):

    percentage = (count/math.factorial(points))*100.0

    font = pygame.font.SysFont("Times New Roman", 25)
    text2 = font.render("Algorithm : Lexicographic Order", True, white)
    display.blit(text2, (70, 10))

    text = font.render("{0:.2f}".format(percentage) + " % Completed", True, white)
    display.blit(text, (width/2 + 100, 10))

    for i in range(len(order)):
        index = order[i]
        pygame.draw.ellipse(display, white, (cities[index].x, cities[index].y, d, d))

    for i in range(len(order)-1):
        pygame.draw.line(display, white, (cities[order[i]].x + d/2, cities[order[i]].y+d/2), (cities[order[i+1]].x+d/2, cities[order[i+1]].y+d/2), 1)

    for i in range(len(order) - 1):
        pygame.draw.line(display, purple, (width/2 + cities[bestEverOrder[i]].x + d / 2, cities[bestEverOrder[i]].y + d / 2),
                         (width/2 + cities[bestEverOrder[i + 1]].x + d / 2, cities[bestEverOrder[i + 1]].y + d / 2), 3)

    for i in range(len(bestEverOrder)):
        index = bestEverOrder[i]
        pygame.draw.ellipse(display, white, (width/2 + cities[index].x, cities[index].y, d, d))


def next_order():
    global order, count, x
    x = -1
    count += 1.0
    for i in range(len(order) - 1):
        if order[i] < order[i + 1]:
            x = i
    y = 0
    for j in range(len(order)):
        if order[x] < order[j]:
            y = j

    swap(order, x, y)

    order[x + 1:] = reversed(order[x + 1:])


def swap(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp


def total_distance(a):
    dist = 0
    for i in range(len(order)-1):
        dist += math.sqrt((a[order[i]].x - a[order[i+1]].x)**2 + (a[order[i]].y - a[order[i+1]].y)**2)

    return dist


def pauseUnpause():
    global pause

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    pause = False

    main_loop()


main_loop()
