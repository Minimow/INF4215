# -*- coding: utf-8 -*-

from state import *
from point import *
from localSearch import *
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
        for x in range(0, len(self.towers)):
            print map(str, self.towers[x])

    # State is updated according to action
    def executeAction(self,(action, towerId, houseId)):
        if action == 'addRange':
            tower = self.towers[towerId]
            newRadius = Point.distanceToPoint(tower[0], self.houses[houseId])
            self.towers[towerId][1] = math.ceil(newRadius)
            self.removeIncludedHouses(tower)
        elif action == "addTower":
            radius = Point.distanceToPoint(self.availablesPositions[towerId], self.houses[houseId])
            if (radius < 1):
                radius = 1
            newTower = [self.availablesPositions[towerId], math.ceil(radius)]
            self.towers.append(newTower)
            self.availablesPositions.pop(towerId)
            self.removeIncludedHouses(newTower)
        elif action == "removeTower":
            return 0
        elif action =="rem55ove":
            return 0

    def removeIncludedHouses(self, tower):
        housesLeft = copy.deepcopy(self.houses)

        for i in range(0, len(self.houses)):
            tPosition = tower[0]
            if Point.distanceToPoint(tPosition, self.houses[i]) <= tower[1]:
                print "unreached"
                print ','.join(map(str, self.unreached))
                print "house to remove"
                print self.houses[i]
                if self.houses[i] in self.unreached:
                    self.unreached.remove(self.houses[i])

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
        return len(self.unreached) * minimalCost / len(self.houses)

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
    simulated_annealing_search(initialState)

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
                return node
            else:
                candidate = random.choice(node.expand())
                if candidate.h < node.h:
                    node = candidate
                elif random.random() < math.exp(float(node.h - candidate.h)/temperature):
                    node = candidate
                step -= 1
        temperature = decrease(temperature)
    return None

print "hello"
positions = [Point(6,0), Point(2,2), Point(4,4), Point(6,8), Point(10,8)]
K = 200
C = 1
search(positions, K, C)

