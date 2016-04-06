from Controller import *
from AI import *
from RandomAI import *
from CustomAI import *

ai1 = AI() # agent adverse sans apprentissage machine


nbWinAI2 = 0
for i in xrange(100):
    ai2 = CustomAI(False) # agent adverse aleatoire
    controller = Controller("Americas", "Normal", "Custom", ai1, ai2)
    winningPlayerIndex = controller.play()
    if winningPlayerIndex == 1:
        nbWinAI2 += 1
print "Nb win of ai2 : ", nbWinAI2