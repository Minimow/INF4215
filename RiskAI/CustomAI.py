from random import Random
from AI import AI
from AttackAction import AttackAction
from MoveAction import MoveAction
from PlaceTroopsAction import PlaceTroopsAction
import json

__author__ = 'Julien'


class CustomAI(AI):

    def __init__(self):
        self.random = Random()
        self.random.seed()

        self.magicNumbers = self.loadMagicNumbers()
        #AI magic numbers
        #self.ratioStopAttack = 1 # if the ratio troops/ennemyTroops is under, we cancel the attack
        #self.ennemiesForHostileTerritory = 2  # If a country has more ennemy than this value, the country is in a hostile territory

        bestChoiceChance = 90 # % of chance to take the best choice available other time its random
        self.ratioStopAttack = self.getMagicNumbersValue(self.magicNumbers["ratioStopAttack"], bestChoiceChance)
        self.ennemiesForHostileTerritory = self.getMagicNumbersValue(self.magicNumbers["ennemiesForHostileTerritory"], bestChoiceChance)

    def loadMagicNumbers(self):
        with open('magicNumbers.txt') as data_file:
            data = json.load(data_file)
        return data

    def getMagicNumbersValue(self, data, chanceOfBest):

        if self.random.randrange(0, 100) < chanceOfBest:
            bestRating = 0
            bestData = 0

            for value in data:
                if data[value] > bestRating:
                    bestData = value
                    bestRating = data[value]

            return bestData
        else:
            randomKey = self.random.choice(data.keys())
            return randomKey

    def writeNewMagicNumbers(self, data):
        with open('magicNumbers.txt', 'w') as data_file:
            json.dump(data, data_file)

    def isCountryInHostileTerritory(self, country):
        count = self.numberOfEnnemies(country)
        return count >= self.ennemiesForHostileTerritory

    def numberOfEnnemies(self, country):
        count = 0
        for neighbour in country.getNeighbours():
                if neighbour.getOwner() != country.getOwner():
                    count += 1
        return count

    # Choose a starting country one at the time
    #
    # remainingCountries : the countries that are not chosen yet
    # ownedCountries : the countries that you own so far
    # allCountries : all countries
    #
    # return : Try to pick a country adjacent to one you already own. If not possible pick at random
    def chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries):
        for ownedCountry in ownedCountries:
            for neighbour in ownedCountries[ownedCountry].getNeighbours():
                if neighbour in remainingCountries:
                    return neighbour
        return self.random.choice(remainingCountries)

    # Place troops before the games begins. You can place only a portion of the available
    # troops. This method will be called again if you still have troops to be placed
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeStartingTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        return self.placeTroops(nbTroopsToPlace, ownedCountries, allCountries)

    # Declare attacks on the other countries. You need to check if the defending country is
    # not yours, or your attack declaration will be ignored
    #
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : For now only attacks when higher than the alwaysAttack Ratio
    def declareAttacks(self, ownedCountries, allCountries):
        allPossibilities = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            for neighbour in country.getNeighbours():
                # can attack the neighbour
                if neighbour.getOwner() != country.getOwner():
                    if country.getNbTroops() / neighbour.getNbTroops() >= float(self.ratioStopAttack):
                        allPossibilities.append(AttackAction(country, neighbour, 3))

        return allPossibilities

    # Place troops at the start of your turn. You need to place all available troops at one
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : Place troops evenly in hostile territory, if no hostile territory plce evenly in countries next to an ennemy
    def placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        placeTroopsAction = []
        rest = nbTroopsToPlace
        hostileCountries = []
        hasEnnemiesCountries = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            isHostile = self.isCountryInHostileTerritory(country)
            if isHostile:
                hostileCountries.append(country)
            if self.numberOfEnnemies(country) > 0:
                hasEnnemiesCountries.append(country)

        if len(hostileCountries) > 0:
            troopsPerCountry = nbTroopsToPlace / len(hostileCountries)
            for hostileCountry in hostileCountries:
                placeTroopsAction.append(PlaceTroopsAction(hostileCountry.getName(), troopsPerCountry))
                rest -= troopsPerCountry
        else:
            troopsPerCountry = nbTroopsToPlace / len(hasEnnemiesCountries)
            for hostileCountry in hasEnnemiesCountries:
                placeTroopsAction.append(PlaceTroopsAction(hostileCountry.getName(), troopsPerCountry))
                rest -= troopsPerCountry

        while rest > 0:
            troopAction = self.random.choice(placeTroopsAction)
            toAdd = self.random.randint(1, rest)
            troopAction.nbTroops += toAdd
            rest -= toAdd

        return placeTroopsAction

    # Move troops after attacking. You can only move one per turn
    #
    # turnAttackResults : the result of all the attacks you declared this turn
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : Find countries in hostile territory. Give troops from the best neighboors (highest troops without ennemy).
    def moveTroops(self, turnAttackResults, ownedCountries, allCountries):
        possibleMoves = []

        hostileCountries = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            isHostile = self.isCountryInHostileTerritory(country)
            if isHostile:
                hostileCountries.append(country)

        for hostileCountry in hostileCountries:
            bestNeighbour = None
            for neighbour in hostileCountry.getNeighbours():
                if neighbour.getOwner() == hostileCountry.getOwner():
                    # bestNeighbour if the neighbour is not in a hostile territory and if it has more troops than the current best.
                    if (bestNeighbour == None or neighbour.getNbTroops() > bestNeighbour.getNbTroops())\
                            and not self.isCountryInHostileTerritory(neighbour):
                        bestNeighbour = neighbour
            if(bestNeighbour != None):
                return MoveAction(bestNeighbour, hostileCountry, bestNeighbour.getNbTroops() -1)

        return None


    # Decide the amount of attacking dice while attacking
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 0 and 3, 0 means that you want to cancel the attack
    #
    # default behaviour : always choose 3
    def decideNbAttackingDice(self, attackResult, ownedCountries, allCountries):
        country = attackResult._attackingCountry
        ennemyCountry = attackResult._defendingCountry
        if not (ennemyCountry.getNbTroops() == 0):
            ratio = country.getNbTroops() / ennemyCountry.getNbTroops()
            if (ratio  < self.ratioStopAttack):
                return 0

        return 3

    # Decide the amount of defending dice while defending
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 1 and 2
    #
    # default behaviour : always choose 2
    def decideNbDefendingDice(self, attackResult, ownedCountries, allCountries):
        return 2

    # Decide the amount of troops to be transfered to the new country after winning a battle
    #
    # attackResult : the result of the attack
    # startCountry : the country to move from
    # endCountry : the country to move to
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 1 and the amount of troops in startCountry
    #
    # default behaviour : if the new country is hostile, move all troops. if not random.
    def decideNbTransferingTroops(self, attackResult, startCountry, endCountry, ownedCountries, allCountries):
        newTerritoryHostile = self.isCountryInHostileTerritory(endCountry)

        # if hostile we move everything
        if newTerritoryHostile:
            return startCountry.getNbTroops() -1
        # if the new country has no ennemy we move only 1 troop
        elif self.numberOfEnnemies(endCountry) == 0:
            return 1
        else:
            return self.random.randint(1, startCountry.getNbTroops() - 1)

    # Called when your AI wins an attack
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onAttackWon(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI loses an attack. AKA the attack finished because you only have 1 troop left in
    # the attacking country
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onAttackLost(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI succeeds to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onDefendWon(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI fails to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onDefendLost(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI wins the game
    #
    # allCountries : all countries, you own all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onGameWon(self, allCountries):
        data = self.loadMagicNumbers()
        oldRatioToAlwaysAttack = data["ratioStopAttack"][str(self.ratioStopAttack)]
        data["ratioStopAttack"][str(self.ratioStopAttack)] = oldRatioToAlwaysAttack + 1

        oldEnnemiesForHostileTerritory = data["ennemiesForHostileTerritory"][str(self.ennemiesForHostileTerritory)]
        data["ennemiesForHostileTerritory"][str(self.ennemiesForHostileTerritory)] = oldEnnemiesForHostileTerritory + 1

        self.writeNewMagicNumbers(data)

    # Called when your AI lost the game
    #
    # allCountries : all countries, you own no countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onGameLost(self, allCountries):
        data = self.loadMagicNumbers()
        oldRatioToAlwaysAttack = data["ratioStopAttack"][str(self.ratioStopAttack)]
        data["ratioStopAttack"][str(self.ratioStopAttack)] = oldRatioToAlwaysAttack - 1

        oldEnnemiesForHostileTerritory = data["ennemiesForHostileTerritory"][str(self.ennemiesForHostileTerritory)]
        data["ennemiesForHostileTerritory"][str(self.ennemiesForHostileTerritory)] = oldEnnemiesForHostileTerritory - 1

        self.writeNewMagicNumbers(data)

