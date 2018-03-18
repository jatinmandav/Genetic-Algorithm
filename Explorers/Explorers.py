import pygame
import sys
from math import *
import random

pygame.init()

width = 800
height = 600

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Explorers")

background = (51, 51, 51)
white = (240, 240, 240)
light_red = (203, 67, 53)
gray = (123, 125, 125)

h = 15
w = 8

totalPopulation = 250
mutation_rate = 3
lifespan = 300
count = 0
generation = 0
var = 0

targetw = 30
targeth = 30
targetx = width/2- targetw/2
targety = 10
targetCx = targetx + targetw/2
targetCy = targety + targeth/2

obsw = 300
obsh = 20

obs1x = 30
obs1y = height/2 - 100

obs2x = width - obsw - 30
obs2y = height/2 - 100

obs3x = width/2 - obsw/2
obs3y = height/2 + 100


def draw_line(x1, y1, x2, y2):
    pygame.draw.line(display, white, (x1, y1), (x2, y2), w)


def heuristics(x, y):
    #return sqrt(pow(x-targetCx, 2) + pow(y-targetCy, 2))
    return abs(x - targetCx) + abs(y - targetCy)


class DNA:
    def __init__(self):
        self.genes = []
        for i in range(lifespan):
            if random.randint(0, 1):
                self.genes.append(int(10))
            else:
                self.genes.append(int(-10))
                

class Beatle:
    def __init__(self):
        self.angle = 90
        self.x1 = width/2 - w/2
        self.y1 = height - 10 - h
        self.x2 = self.x1 + h*cos(radians(self.angle))
        self.y2 = self.y1 + h*sin(radians(self.angle))
        self.dna = DNA()
        self.moveForward = -3
        self.fitness = 0.0
        self.prob = 0.0
        self.crash = False
        self.completed = False

    def move(self):
        self.angle += self.dna.genes[count]

        self.x1 += self.moveForward*cos(radians(self.angle))
        self.y1 += self.moveForward*sin(radians(self.angle))

        if targetx < self.x1 <= targetx + targetw and targety < self.y1 <= targety + targeth:
            self.x1 -= self.moveForward*cos(radians(self.angle))
            self.y1 -= self.moveForward*sin(radians(self.angle))
    
        if obs1x < self.x2 < obs1x + obsw and obs1y < self.y2 < obs1y + obsh:
            self.x1 -= self.moveForward*cos(radians(self.angle))
            self.y1 -= self.moveForward*sin(radians(self.angle))
        elif obs2x < self.x2 < obs2x + obsw and obs2y < self.y2 < obs2y + obsh:
            self.x1 -= self.moveForward*cos(radians(self.angle))
            self.y1 -= self.moveForward*sin(radians(self.angle))
        elif obs3x < self.x2 < obs3x + obsw and obs3y < self.y2 < obs3y + obsh:
            self.x1 -= self.moveForward*cos(radians(self.angle))
            self.y1 -= self.moveForward*sin(radians(self.angle))
        else:
            self.x2 = self.x1 + h*cos(radians(self.angle))
            self.y2 = self.y1 + h*sin(radians(self.angle))

    def draw_beatle(self):
        draw_line(self.x1, self.y1, self.x2, self.y2)

    def calcFitness(self):
        dist = heuristics(self.x2, self.y2)
        if targetx - 1 <= self.x1 <= targetx + targetw + 1 and targety - 1 <= self.y1 <= targety + targeth + 1:
            self.completed = True
        self.fitness = 1.0/(dist + 1)
        if self.completed:
            self.fitness = 0.09


class Population:
    def __init__(self):
        self.population = []
        for i in range(totalPopulation):
            obj = Beatle()
            self.population.append(obj)

    def move(self):
        for i in range(totalPopulation):
            self.population[i].move()
            
    def show(self):
        for i in range(totalPopulation):
            self.population[i].draw_beatle()

    def calcFitness(self):
        for i in range(totalPopulation):
            self.population[i].calcFitness()

    def normalizeFitness(self):
        fitnessSum = 0.0
        for i in range(totalPopulation):
            fitnessSum += self.population[i].fitness

        for i in range(totalPopulation):
            self.population[i].prob = self.population[i].fitness/fitnessSum

    def reproduce(self):
        for i in range(totalPopulation):
            indexA = pickOne(self.population)
            indexB = pickOne(self.population)

            child = DNA()
            child.genes = self.crossover(self.population[indexA].dna.genes, self.population[indexB].dna.genes)
            self.population[i].dna.genes = list(child.genes)
            self.population[i].dna.genes = self.mutate(self.population[i].dna.genes)


    def crossover(self, a1, a2):
        mid = random.randrange(0, lifespan)

        a3 = DNA()
        for i in range(lifespan):
            if i > mid:
                a3.genes[i] = a1[i]
            else:
                a3.genes[i] = a2[i]

        return a3.genes

    def mutate(self, a):
        prob = random.randrange(0, 100)
        index = random.randrange(0, lifespan)
        if prob < mutation_rate:
            if random.randint(0, 1):
                a[index] = 10
            else:
                a[index] = -10

        return a

    def reset(self):
        for i in range(totalPopulation):
            self.population[i].angle = 90
            self.population[i].x1 = width/2 - w/2
            self.population[i].y1 = height - 10 - h
            self.population[i].x2 = self.population[i].x1 + h*cos(radians(self.population[i].angle))
            self.population[i].y2 = self.population[i].y1 + h*sin(radians(self.population[i].angle))
            self.population[i].crash = False
            self.population[i].completed = False


def pickOne(population):
    prob = random.uniform(0, 1)

    for i in range(totalPopulation):
        prob -= population[i].prob
        if prob < 0:
            return i


def target():
    pygame.draw.rect(display, light_red, (targetx, targety, targetw, targeth))


def show_obstacles():
    pygame.draw.rect(display, gray, (obs1x, obs1y, obsw, obsh))
    pygame.draw.rect(display, gray, (obs2x, obs2y, obsw, obsh))
    pygame.draw.rect(display, gray, (obs3x, obs3y, obsw, obsh))


def display_info():
    global var
    font = pygame.font.SysFont("Times New Roman", 18)
    text1 = font.render("Generation : " + str(generation), True, white)
    text2 = font.render("Population Size : " + str(totalPopulation), True, white)
    text3 = font.render("Muatation Rate : " + str(mutation_rate) + " %", True, white)
    
    display.blit(text1, (10, 10))
    display.blit(text2, (10, 30))
    display.blit(text3, (10, 50))
    

def close():
    pygame.quit()
    sys.exit()
    

def main_loop():
    loop = True
    global count, generation, reachedTarget
    generation = 0
    
    population = Population()
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    main_loop()

        display.fill(background)

        population.move()
        population.show()

        count += 1

        if count == lifespan - 1:
            count = 0
            population.calcFitness()
            population.normalizeFitness()
            
            population.reproduce()
            population.reset()
            generation += 1


        display_info()
        target()
        show_obstacles()
                
        pygame.display.update()
        clock.tick(60)

main_loop()
    
