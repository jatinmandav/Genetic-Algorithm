# -----------------------------------------------------------------------------
#
# Solving the Shakespeare-Monkey Problem Using Genetic Algorithm
#
# Language - Python
# Modules - pygame, sys, random
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

pygame.init()

width = 800
height = 300

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Genetic Algorithm : Shakespeare - Monkey Problem")
clock = pygame.time.Clock()

background = (51, 51, 51)
white = (240, 243, 244)

phraseToEvolve = "Genetic Algorithm"
init__population = 200
mutation_rate = 8
population = []

small_font = pygame.font.SysFont("Times New Roman", 22)
large_font = pygame.font.SysFont("Times New Roman", 40)

# DNA of each population Individual
class DNA:
    def __init__(self, target, mutation_rate):
        self.genes = []
        self.fitness = 0.0
        self.target_phrase = target
        for i in range(len(target)):
            newchar = newChar()
            self.genes.append(newchar)
        self.mutation_rate = mutation_rate
        self.phenotype = ''.join(self.genes)

    def calcFitness(self):
        score = 0.0
        for i in range(len(self.target_phrase)):
            if self.genes[i] == self.target_phrase[i]:
                score += 1.0

        self.fitness = float(score/len(self.target_phrase))

        self.phenotype = ''.join(self.genes)

    def crossover(self, partner):
        midpoint = random.randrange(1, len(self.genes))

        child = DNA(self.target_phrase, self.mutation_rate)

        for i in range(len(self.genes)):
            if i < midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]

        index = random.randrange(0, len(self.genes))
        char = self.mutate()
        if char:
            child.genes[index] = char

        return child

    def mutate(self):
        prob = random.randrange(0, 100)
        if prob < self.mutation_rate:
            return newChar()

    def check(self):
        if self.fitness == 1.0:
            return True
        else:
            return False

# Population Class
class Population:
    def __init__(self, target_phrase, population_length, mutation):
        self.target = target_phrase
        self.totalPopulation = population_length
        self.population = [[]for _ in range(self.totalPopulation)]
        self.mutation_rate = mutation
        self.generation = 0

    def create_population(self):
        for i in range(self.totalPopulation):
            self.population[i] = DNA(self.target, self.mutation_rate)

    def calculate_fitness(self):
        for i in range(self.totalPopulation):
            self.population[i].calcFitness()

        self.blit_text()
        for i in range(self.totalPopulation):
            if self.population[i].check():
                pause()

    def reproduce(self):
        self.generation += 1
        for i in range(self.totalPopulation):
            partnerA = self.pickParent()
            partnerB = self.pickParent()
            child = partnerA.crossover(partnerB)
            self.population[i] = child

    def pickParent(self):
        prob = random.uniform(0, 1)
        for i in range(self.totalPopulation):
            prob -= self.population[i].fitness
            if prob < 0.0:
                return self.population[i]

        indexRandom = random.randrange(0, self.totalPopulation)
        return self.population[indexRandom]

    def blit_text(self):

        best = large_font.render("Best Match So Far : ", True, white)
        best_match = large_font.render(self.fittest(), True, white)
        generation = small_font.render("Total Generations : " + str(self.generation), True, white)
        pop = small_font.render("Population : " + str(self.totalPopulation), True, white)
        mutate = small_font.render("Mutation Rate : " + str(self.mutation_rate) + "%", True, white)

        display.blit(best, (30, 40))
        display.blit(best_match, (30, 100))

        display.blit(generation, (30, 175))
        display.blit(pop, (30, 200))
        display.blit(mutate, (30, 225))

        pygame.display.update()

    def fittest(self):
        fittestScore = self.population[0].fitness
        index = 0
        for i in range(self.totalPopulation):
            if self.population[i].fitness > fittestScore:
                fittestScore = self.population[i].fitness
                index = i

        return self.population[index].phenotype

    def checkCorrectness(self):
        for i in range(self.totalPopulation):
            if self.population[i].fitness == 1.0:
                print("Perfect Match!")


def newChar():
    i = random.randrange(63, 123)
    if i == 63:
        i = 32
    if i == 64:
        i = 46
    return chr(i)


def reset():
    global population
    population = Population(phraseToEvolve, init__population, mutation_rate)


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main_loop():
    loop = True
    global population
    reset()

    population.create_population()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        display.fill(background)

        population.calculate_fitness()

        population.reproduce()

        population.checkCorrectness()

        pygame.display.update()
        clock.tick(60)


main_loop()
