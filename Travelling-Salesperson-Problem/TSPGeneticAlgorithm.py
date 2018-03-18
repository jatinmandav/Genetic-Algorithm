# -----------------------------------------------------------------------------
#
# TSP using Genetic Algorithm
#
# Language - Python
# Modules - pygame, sys, random, math
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

pygame.init()

width = 800
height = 600

# Setup Screen
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("TSP Genetic Algorithm")
clock = pygame.time.Clock()

background = (51, 51, 51) 
white = (240, 240, 240)
purple = (136, 78, 160)

# Initialize Variables and basic Information
totalCities = 10
cities = []
totalPopulation = 10
generation = 0

bestEver = []
currentBest = []
highestFitness = 0
initial_order = []

shortestDist = 0
currentDist = 0

mutation_rate = 2

d = 10

# Quit Pygame Window
def quit_window():
    pygame.quit()
    sys.exit()

# DNA of Population
class DNA:
    def __init__(self, order):
        # Initialize the Variables
        self.genes = []
        self.fitness = 0.0
        self.order = order
        self.prob = 0.0
        self.distance = 0

    # Create Genes
    def createGenes(self):
        self.genes = shuffle_list(self.order, 100)

    # Calculate Fitness of DNA, Gene
    def calcFitness(self):
        totalDist = 0.0
        for i in range(len(self.genes)-1):
            dist = ((cities[self.genes[i]][0] - cities[self.genes[i+1]][0])**2 + (cities[self.genes[i]][1] - cities[self.genes[i+1]][1])**2)**0.5
            totalDist += dist

        self.distance = totalDist
        self.fitness = 1.0/(totalDist)*10
        
# Shuffle a list n times
def shuffle_list(order, n):
    for i in range(n):
        a = random.randrange(0, len(order))
        b = random.randrange(0, len(order))
        order = swap(order, a, b)
    return order

# Swap two Elements in list
def swap(l, i, j):
    temp = l[i]
    l[i] = l[j]
    l[j] = temp

    return l

# Create Population of routes
class Population:
    def __init__(self):
        # Initialize Variables
        self.population = []
        for i in range(totalPopulation):
            dnaObj = DNA(initial_order)
            dnaObj.createGenes()
            self.population.append(dnaObj)

    # Calculate Fitness of Population
    def calcFitness(self):
        for i in range(totalPopulation):
            self.population[i].calcFitness()
        self.normalizeFitness()

    # Normalize the Fitness 
    def normalizeFitness(self):
        total = 0.0
        for i in range(totalPopulation): 
            total += self.population[i].fitness
        
        for i in range(totalPopulation):
            self.population[i].prob = self.population[i].fitness/total
            format(self.population[i].prob, '.3f')
            
    # Reproduce next Generation from previous generation
    def reproduce(self):
        global generation
        for i in range(totalPopulation):
            indexA = pickOne(self.population)
            indexB = pickOne(self.population)
            child = DNA([])
            child.genes = self.crossover(self.population[indexA].genes, self.population[indexB].genes)
            self.population[i].genes = child.genes[:]
            self.population[i].genes = self.mutate(self.population[i].genes)
        generation += 1

    # Perform Crossover on two genes
    def crossover(self, parentAGenes, parentBGenes):
        start = random.randrange(0, len(parentAGenes))
        end = random.randrange(start, len(parentAGenes))

        parentAGenes = parentAGenes[start: end]

        for i in range(len(parentBGenes)):
            if parentBGenes[i] not in parentAGenes:
                parentAGenes.append(parentBGenes[i])
        return parentAGenes

    # Mutate a gene based on Mutation Rate
    def mutate(self, genes):
        num = random.randrange(0, 100)

        if num <= mutation_rate:
            indexA = random.randrange(0, len(genes))
            indexB = indexA + 1
            if indexB >= totalCities:
                indexB = indexA - 1
            swap(genes, indexA, indexB)

        return genes

    # Find the Fittest member of generation
    def findBest(self):
        global bestEver, currentBest, highestFitness, shortestDist, currentDist
        fitScore = 0.0
        for i in range(totalPopulation):
            if self.population[i].fitness > fitScore:
                fitScore = self.population[i].fitness
                currentBest = self.population[i].genes[:]
                currentDist = self.population[i].distance
        for i in range(totalPopulation):
            if self.population[i].fitness > highestFitness:
                highestFitness = self.population[i].fitness
                bestEver = self.population[i].genes[:]
                shortestDist = self.population[i].distance
        
#Pick a member according to Probability
def pickOne(population):
    prob = random.uniform(0, 1)
    for i in range(totalPopulation):
        prob -= population[i].prob
        if prob < 0:
            return i

# Draw Current and all time best routes
def draw_bestEver():
    for i in range(len(bestEver)-1):
        pygame.draw.line(display, purple, (width/2 + cities[bestEver[i]][0] + d/2, cities[bestEver[i]][1] + d/2), (width/2 + cities[bestEver[i+1]][0] + d/2, cities[bestEver[i+1]][1] + d/2), 3)
    for i in range(totalCities):
        pygame.draw.ellipse(display, white, (width/2 + cities[i][0], cities[i][1], d, d))
        
    
    for i in range(totalCities):
        pygame.draw.ellipse(display, white, (cities[i][0], cities[i][1], d, d))

    for i in range(len(bestEver)-1):
        pygame.draw.line(display, white, (cities[currentBest[i]][0] + d/2, cities[currentBest[i]][1] + d/2), (cities[currentBest[i+1]][0] + d/2, cities[currentBest[i+1]][1] + d/2), 1)

# Add Information on Screen
def add_information():
    font = pygame.font.SysFont("Times New Roman", 25)
    text2 = font.render("Algorithm : Genetic Algorithm", True, white)
    display.blit(text2, (width / 2 - 140, 10))

    font = pygame.font.SysFont("Times New Roman", 20)
    currentDistText = font.render("Generation Best Result : " + str(currentDist), True, white)
    display.blit(currentDistText, (10, height - 150))
    
    currentDistText = font.render("Shortest Distance so far : " + str(shortestDist), True, white)
    display.blit(currentDistText, (width/2 + 10, height - 150))

    generationText = font.render("Generation : " + str(generation), True, white)
    display.blit(generationText, (75, height-50))
    
    populationText = font.render("Population : " + str(totalPopulation), True, white)
    display.blit(populationText, (width/2 - 100, height-50))

    mutationText = font.render("Mutation Rate : " + str(mutation_rate), True, white)
    display.blit(mutationText, (width/2 + 100, height-50))

#Reset the Population and Cities
def reset():
    global cities, generation, bestEver, currentBest, highestFitness, shortestDist, currentDist, initial_order
    cities = []
    generation = 0

    initial_order = []
    
    bestEver = []
    currentBest = []
    highestFitness = 0

    shortestDist = 0
    currentDist = 0

# Algorithm Works Here
def main_loop():
    loop = True
    global totalCities
    reset()
    
##    for i in range(totalCities):
##        x = random.randrange(10, width/2 - 10)
##        y = random.randrange(40, height-210)
##        cities.append([x, y])
##        initial_order.append(i)
        
    pointsF = open("points.txt", "r")
    data = pointsF.readlines()
    pointsF.close()
    totalCities = len(data)
    for i in range(len(data)):
        data[i] = data[i].split(" ")
        data[i][0] = int(data[i][0])
        data[i][1] = int(data[i][1])

    for i in range(len(data)):
        initial_order.append(i)
        cities.append([data[i][0], data[i][1]])


    population = Population()
        
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_window()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_window()
                if event.key == pygame.K_r:
                    main_loop()

        display.fill(background)

        # Step 1 : Calculate Fitness of population
        
        population.calcFitness()
        population.findBest()

        # Step 2 : Generaate New Population using old population
        
        population.reproduce()

        # Step 3 : Put Everything On Screen for Display
        
        add_information() 
        draw_bestEver()

        pygame.display.update()
        clock.tick(60)


main_loop()
