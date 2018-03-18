# -----------------------------------------------------------------------------
#
# Evolving a Random Image using Genetic Algorithm
#
# Language - Python
# Modules - pygame, sys, random, time
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
import time

pygame.init()

width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Evolving Image Using Genetic Algorithm")
clock = pygame.time.Clock()

# Colors
black = (51, 51, 51)
blue = (46, 134, 193)
red = (203, 67, 53)
yellow = (241, 196, 15)

white = (236, 240, 241)

# Color list from which image is to be generated and Evolved
colorList = [red,white, blue]

pixelSize = 20
picW = 10
picH = 10

font = pygame.font.SysFont("Times New Roman", 22)

bestMatch = 0
matchPercent = 0.0

popSize = 50
mutationRate = 5

generation = 1

# Each Pixel Class
class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# Picture Class
class Picture:
    def __init__(self):
        self.picture = []
        self.fitness = 0
        self.prob = 0
        self.match = 0

    # Create a Smiley Image
    def createSmiley(self, initX, initY):
        for i in range(picH):
            self.picture.append([])
            for j in range(picW):
                x = initX + i*pixelSize
                y = initY + j*pixelSize
                if j == 0 or j == 9 or i == 0 or i == 9:
                     newObj = Pixel(x, y, colorList[0])
                elif (i == 3 and j == 3) or (j == 3 and i == 6):
                    newObj = Pixel(x, y, colorList[0])
                elif (j == 5) and (i == 2 or i == 7):
                    newObj = Pixel(x, y, colorList[0])
                elif j == 6 and (3 <= i <= 6):
                    newObj = Pixel(x, y, colorList[0])
                elif (j == 1 or j == 8) and (i == 1 or i == 2 or i == 7 or i == 8):
                    newObj = Pixel(x, y, colorList[0])
                elif (j == 2 or j == 7) and (i == 1 or i == 8):
                    newObj = Pixel(x, y, colorList[0])
                else:
                    newObj = Pixel(x, y, colorList[1])

                self.picture[i].append(newObj)

    # Create a random Image Pattern using colorList
    def createPic(self, initX, initY):
        for i in range(picH):
            self.picture.append([])
            for j in range(picW):
                x = initX + i*pixelSize
                y = initY + j*pixelSize
                newObj = Pixel(x, y, random.choice(colorList))
                self.picture[i].append(newObj)

    def drawPic(self):
        for i in range(picH):
            for j in range(picW):
                pygame.draw.rect(display, self.picture[i][j].color, (self.picture[i][j].x, self.picture[i][j].y, pixelSize, pixelSize))

    def calcFitness(self, targetPic):
        error = 0
        for i in range(picH):
            for j in range(picW):
                if not (targetPic.picture[i][j].color[0] == self.picture[i][j].color[0]):
                    error += 1
        self.fitness = 1.0/(error + 1)
        self.match = ((float((picW*picH) - error))/(picW*picH))*100
        
# Population Class    
class Population:
    def __init__(self):
        self.population = []

    def createPop(self):
        for i in range(popSize):
            newPic = Picture()
            newPic.createPic(width/2 + 50, 50)
            self.population.append(newPic)

    def calcFitness(self, targetPic):
        for i in range(popSize): 
            self.population[i].calcFitness(targetPic)

        self.normalizeFitness()

    def normalizeFitness(self):
        global bestMatch, matchPercent
        fitSum = 0.0
        for i in range(popSize):
            fitSum += self.population[i].fitness

        for i in range(popSize):
            self.population[i].prob = self.population[i].fitness/fitSum
            
        bestMatch = self.population[0]
        matchPercent = 0.0
        
        for i in range(popSize):
            if self.population[i].prob > matchPercent:
                matchPercent = self.population[i].match
                bestMatch = self.population[i]

    def reproduce(self):
        global generation
        newPopulation = []
        for i in range(popSize):
            index1 = pickOne(self.population)
            index2 = pickOne(self.population)

            newObj = self.crossover(self.population[index1].picture, self.population[index2].picture)
            newObj.picture = self.mutate(newObj.picture[:])

            newPopulation.append(newObj)

        self.population = newPopulation[:]

        generation += 1
        
    def crossover(self, pic1, pic2):
        newPic = Picture()
        for i in range(picH):
            newPic.picture.append([])
            start = random.randrange(0, picW)
            end = random.randrange(start, picW)
            for j in range(picW):
                if start <= j <= end:
                    color = pic2[i][j].color
                    newPixel = Pixel(width/2 + 50 + i*pixelSize, 50 + j*pixelSize, color)
                    newPic.picture[i].append(newPixel)
                else:
                    color = pic1[i][j].color
                    newPixel = Pixel(width/2 + 50 + i*pixelSize, 50 + j*pixelSize, color)
                    newPic.picture[i].append(newPixel)
        return newPic
                
    def mutate(self, pic):
        prob = random.randrange(0, 100)
        if prob < mutationRate:
            for i in range(picH):
                j = random.randrange(0, picW)
                pic[i][j].color = random.choice(colorList)

        return pic
            

# Pick individual from population according to its fitness
def pickOne(population):
    prob = random.uniform(0, 1)
    for i in range(popSize):
        prob -= population[i].prob
        if prob < 0:
            return i

def close():
    pygame.quit()
    sys.exit()


def mainLoop():

    startTime = time.time()
    
    global generation
    generation = 0
    firstOccurance = 0
    targetPic = Picture()
    #targetPic.createPic(50, 50)
    targetPic.createSmiley(50, 50)

    population = Population()
    population.createPop()

    firstTime = 0
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    mainLoop()

        display.fill(black)

        population.calcFitness(targetPic)
        
        targetPic.drawPic()
        bestMatch.drawPic()

        matchPer = font.render("Match Percent: " + str(matchPercent) + " %", True, white)
        display.blit(matchPer, (width/2 + 50, height - 60))

        if firstOccurance == 0:
            if matchPercent == 100.0:
                firstOccurance = generation
                presentTime = time.time()
                firstTime = presentTime - startTime

        if firstOccurance > 0:
            firstText = font.render("Image First Evolved at " + str(firstOccurance) + " Generation in " + str(firstTime) + " secs!", True, white)
            display.blit(firstText, (25, height - 120))            
        
        population.reproduce()

        tgtText = font.render("Target Image", True, white)
        display.blit(tgtText, (90, 15))

        genBestText = font.render("Generation Best", True, white)
        display.blit(genBestText, (width/2 + 85, 15))

        genText = font.render("Generation: " + str(generation), True, white)
        display.blit(genText, (width/2 + 50, height - 30))

        popText = font.render("Population Size: " + str(popSize), True, white)
        display.blit(popText, (50, height - 60))
        
        mutText = font.render("Mutation Rate: " + str(mutationRate) + " %", True, white)
        display.blit(mutText, (50, height - 30))
        
        presentTime = time.time()
        elapsedTime = presentTime - startTime

        elapText = font.render("Elapsed Time : " + str(elapsedTime) + " Seconds", True, white)
        display.blit(elapText, (50, height - 90))
        
        pygame.display.update()
        clock.tick(60)

mainLoop()
