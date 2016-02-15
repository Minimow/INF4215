from node import *
from localState import *
from point import *
import random

def search(positions, K, C):
    initialState = LocalState([], getAvailablePositions(positions), positions)
    initialState.C = C
    initialState.K = K
    initialState.houses = copy.deepcopy(positions)
    return simulated_annealing_search(initialState)

def getAvailablePositions(positions):
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0

    for i in range(0, len(positions)):
        position = positions[i]

        if position.x < minX:
            minX = position.x
        if position.x > maxX:
            maxX = position.x
        if position.y < minY:
            minY = position.y
        if position.y > maxY:
            maxY = position.y

    availablePositions = []
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            availablePositions.append(Point(x,y))

    return availablePositions

def decrease(t):
    return t*0.9

def simulated_annealing_search(initialState,T = 100,limit = 0.1,maxSteps = 1000):
    temperature = T
    node = Node(initialState)
    while temperature > limit:
        step = maxSteps
        while step > 0:
            if node.state.isGoal():
                node.state.show()
                return copy.deepcopy(node.state)
            else:
                candidate = random.choice(node.expand())
                if candidate.h < node.h:
                    node = candidate
                elif random.random() < math.exp(float(node.h - candidate.h)/temperature):
                    node = candidate
                step -= 1
        temperature = decrease(temperature)
    return None

positions = [Point(6,0), Point(2,2), Point(4,4), Point(6,8), Point(10,8)]
K = 200
C = 1

print "about to search"

bestState = None
while bestState == None:
    bestState = search(positions, K, C)

for i in range(0, 15):
    node = search(positions, K, C)

    if node != None and node.cost("yt") < bestState.cost("ty"):
        print "better"
        bestState = node

print "search ended"
print bestState.show()