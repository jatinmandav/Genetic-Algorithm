import random

width = 800
height = 400

points = 10
cities = open("points.txt", 'w')

for i in range(points):
    x = random.randrange(10, width/2-10)
    y = random.randrange(40, height-10)
    cities.write(str(x) + ' ' + str(y) + '\n')

cities.close()
print("Done!")
