# -----------------------------------------------------------------------------
#
# TSP using Brute Force Method
#
# Language - Python
# Modules - pygame, sys, random, math, copy
#
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
import math
import copy

pygame.init()

width = 800
height = 450

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("TSPBruteForce")

background = (51, 51, 51)
white = (236, 240, 241)
violet = (136, 78, 160)
purple = (99, 57, 116)

points = 8
d = 10

bestEver = []
bestDistance = 0


class Cities:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main_loop():
    loop = True
    cities = []
    global bestEver, bestDistance, points

    font2 = pygame.font.SysFont("Times New Roman", 20)

##    for i in range(points):
##        x = random.randrange(10, width/2-10)
##        y = random.randrange(10, height-10)
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
        i = Cities(data[i][0], data[i][1])
        cities.append(i)

    bestDistance = total_distance(cities)
    bestEver = copy.deepcopy(cities)

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

        i = random.randrange(0, points)
        j = random.randrange(0, points)

        while i == j:
            i = random.randrange(0, points)
            j = random.randrange(0, points)

        swap(cities, i, j)

        distance = total_distance(cities)
        if distance < bestDistance:
            bestDistance = distance
            bestEver = list(cities)

        draw(cities)

        font = pygame.font.SysFont("Times New Roman", 25)
        text2 = font.render("Algorithm : Brute Force", True, white)
        display.blit(text2, (width/2 - 120, 10))

        currenttext = font2.render("Current Distance : " + str(distance), True, white)
        display.blit(currenttext, (50, height-30))

        text = font2.render("Shortest Distance so Far : " + str(bestDistance), True, white)
        display.blit(text, (width/2, height-30))

        pygame.display.update()
        clock.tick(60)


def draw(cities):
    for i in range(points):
        pygame.draw.ellipse(display, white, (cities[i].x, cities[i].y, d, d))

    for i in range(points-1):
        pygame.draw.line(display, white, (cities[i].x + d/2, cities[i].y+d/2), (cities[i+1].x+d/2, cities[i+1].y+d/2), 1)

    for i in range(points - 1):
        pygame.draw.line(display, purple, (width/2 + bestEver[i].x + d / 2, bestEver[i].y + d / 2),
                         (width/2 + bestEver[i + 1].x + d / 2, bestEver[i + 1].y + d / 2), 3)

    for i in range(points):
        pygame.draw.ellipse(display, white, (width/2 + bestEver[i].x, bestEver[i].y, d, d))


def swap(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp


def total_distance(a):
    dist = 0
    for i in range(len(a) - 1):
        dist += math.sqrt((a[i].x - a[i+1].x)**2 + (a[i].y - a[i+1].y)**2)

    return dist


main_loop()
