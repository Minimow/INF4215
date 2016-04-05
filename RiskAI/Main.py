from Controller import *
from AI import *
from RandomAI import *

ai1 = AI() # agent adverse sans apprentissage machine
ai2 = RandomAI() # agent adverse aleatoire

nbWinAI2 = 0
for i in xrange(100):
    controller = Controller("Americas", "Normal", "Random", ai1, ai2)
    winningPlayerIndex = controller.play()
    if winningPlayerIndex == 1:
        nbWinAI2 += 1
print "Nb win of ai2 : ", nbWinAI2