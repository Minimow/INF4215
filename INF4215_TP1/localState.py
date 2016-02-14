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
        self.positions = []

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
    def executeAction(self,action):
        if action == "new":
            newPosition = self.availablesPositions[0]
            houseIndex = self.getNearestHouseIndex(newPosition)
            positionToReach = self.unreached[houseIndex]
            radius = Point.distanceToPoint(newPosition, positionToReach)
            self.towers.append([newPosition, radius])
            del self.availablesPositions[0]
            del self.unreached[houseIndex]
        elif action == "move":
            return 0
        elif action =="remove":
            return 0

    # Returns a list of possible actions with the current state
    def possibleActions(self):
        actions = []
        if self.availablesPositions != []:
            actions.append("new")
        if self.towers != []:
            actions.append("remove")
            actions.append("move")
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
        return len(self.unreached) * minimalCost / len(self.positions)

    def getNearestHouseIndex(self, point):
        index = 0
        minDist = 0
        for i in range(0, len(self.unreached)):
            dist = Point.distanceToPoint(point, self.unreached[i])
            if i == 0:
                minDist = dist
                index = i
            elif dist < minDist:
                minDist = dist
                index = i
        return index

    def getHousesInArea(self, point, radius, houses):
        minX = point.x - radius
        maxX = point.x + radius
        minY = point.y - radius
        maxY = point.y + radius

        index = 0
        indexes = []
        for housePosition in houses:
            if Point.distanceToPoint(point, housePosition) <= radius:
               indexes.append(index)
            index = index + 1
        return indexes

def search(positions, K, C):
    initialState = LocalState([], getAvailablePositions(positions), positions)
    initialState.C = C
    initialState.K = K
    initialState.positions = copy.deepcopy(positions)
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

positions = [Point(30,0), Point(10,10), Point(20,20), Point(30,40), Point(50,40)]
K = 200
C = 1
search(positions, K, C)

