# -*- coding: utf-8 -*-

from state import *
from point import *
from node import *
import sys
import copy
import random

class LocalState(State):
    def __init__(self, towers, availables, unreached):
        #Filled when creating the root state
        self.K = 0
        self.C = 0
        self.houses = []

        #state variables
        # first item is position, second is radius
        self.towers = towers
        # possible location for a tower
        self.availablesPositions = availables
        # unreached towers
        self.unreached = unreached

    # State is changed according to action
    def executeActions(self,action):
        pass

    # Checks whether current state and the one passed as parameter are exactly the same
    def equals(self,state):
        if self.towers == state.towers and self.availablesPositions == state.availablesPositions and self.unreached == state.unreached:
            return True
        else:
            return False

    # Checks whether the state is a goal state
    def isGoal(self):
        return self.unreached == []

    # Prints to the console a description of the state
    def show(self):
        print "cost:" + str(self.cost(""))
        for x in range(0, len(self.towers)):
            print map(str, self.towers[x])

    # State is updated according to action
    def executeAction(self,(action, towerId, houseId)):
        if action == 'addRange':
            tower = self.towers[towerId]
            newRadius = Point.distanceToPoint(tower[0], self.houses[houseId])
            self.towers[towerId][1] = math.ceil(newRadius)
            self.removeIncludedHouses(tower)
            if self.isTowerUnnecessary(tower):
                self.removeTower(towerId)

        elif action == "addTower":
            radius = Point.distanceToPoint(self.availablesPositions[towerId], self.houses[houseId])
            if (radius < 1):
                radius = 1
            newTower = [self.availablesPositions[towerId], math.ceil(radius)]
            self.towers.append(newTower)
            self.availablesPositions.pop(towerId)
            self.removeIncludedHouses(newTower)
        elif action == "removeTower":
            self.removeTower(towerId)
        elif action =="move":
            return 0

    #Remove tower from the list
    def removeTower(self, towerIndex):
        housesAffected = self.getHousesForTower(self.towers[towerIndex])
        for i in range(0, len(housesAffected)):
            if len(self.getTowersForHouse(housesAffected[i])) <= 1:
                self.unreached.append(housesAffected[i])

        del self.towers[towerIndex]

    #Update self.unreached base on the tower pssed in parameter
    def removeIncludedHouses(self, tower):
        for i in range(0, len(self.houses)):
            tPosition = tower[0]
            if Point.distanceToPoint(tPosition, self.houses[i]) <= tower[1]:
                if self.houses[i] in self.unreached:
                    self.unreached.remove(self.houses[i])

    # Get all towers that cover the house
    def getTowersForHouse(self, house):
        towers = []

        for i in range(0, len(self.towers)):
            tPosition = self.towers[i][0]
            if Point.distanceToPoint(tPosition, house) <= self.towers[i][1]:
                towers.append(self.towers[i])

        return towers

    # Return true if the tower cover only points that are already covered
    def isTowerUnnecessary(self, tower):
        coveredHouses = self.getHousesForTower(tower)
        for i in range(0, len(coveredHouses)):
            towerCoveringHouse = self.getTowersForHouse(coveredHouses[i])
            if len(towerCoveringHouse) < 2:
                return False
        return True


    # get all houses(points) covered by the tower
    def getHousesForTower(self, tower):
        houses = []

        for i in range(0, len(self.houses)):
            tPosition = tower[0]
            if Point.distanceToPoint(tPosition, self.houses[i]) <= tower[1]:
                houses.append(self.houses[i])

        return houses

    # Returns a list of possible actions with the current state
    def possibleActions(self):
        actions = []
        for i in range(len(self.availablesPositions)):
            actions.append(('addTower', i, self.closestHouse(self.availablesPositions[i])))
        if len(self.towers) > 0:
            for i in range(len(self.towers)):
                actions.append(('addRange', i, self.closestHouse(self.availablesPositions[i])))
            for i in range(len(self.towers)):
                actions.append(('removeTower', i, self.closestHouse(self.availablesPositions[i])))
        return actions

    # Returns the cost of executing some action
    # By default, we suppose that all actions have the same cost = 1
    def cost(self,action):
        cost = 0
        for tower in self.towers:
            r2 = pow(tower[1],2)
            unitCost = self.K + (self.C*r2)
            cost += unitCost
        return cost

    # Returns a heuristic value that provides an estimate of the remaining
    # cost to achieve the goal
    # By default, value is 0
    def heuristic(self):
        minimalCost = min(self.K, self.K + (self.C))
        return len(self.unreached) * minimalCost

    def closestHouse(self, position):
            nbHouses = len(self.houses)
            min = sys.maxint
            candidat = 0
            for i in range(nbHouses):
                house = self.houses[i]
                distPoint = Point.distanceToPoint(house, position)
                if(distPoint < min):
                    min = distPoint
                    candidat = i
            return candidat

def search(positions, K, C):
    initialState = LocalState([], getAvailablePositions(positions), positions)
    initialState.C = C
    initialState.K = K
    initialState.houses = copy.deepcopy(positions)
    return simulated_annealing_search(initialState)

# get the size of the grid based on the position of the houses(points)
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

def simulated_annealing_search(initialState,T = 120,limit = 0.1,maxSteps = 1000):
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

bestState = None
while bestState == None:
    bestState = search(positions, K, C)

for i in range(0, 15):
    node = search(positions, K, C)

    if node != None and node.cost("yt") < bestState.cost("ty"):
        bestState = node

print bestState.show()



