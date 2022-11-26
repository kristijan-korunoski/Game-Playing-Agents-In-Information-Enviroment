# Kristijan Korunoski   - 22966841
# Amandeep Singh        - 22904833

import random
from array import *
import matplotlib
import matplotlib.pyplot as plt
import igraph as ig
matplotlib.rcParams['interactive'] = True


def createGrey(numGrey, numSpy):
    grey = []
    for i in range(numGrey):
        if i < numSpy:
            grey.append(0)  # 0 represents spy
        else:
            grey.append(1)
    return grey


def createGreen(number, avgConnections):
    global EnergyLevel
    greenLinks = []
    numConnectDict = {}
    personalConnectDict = {}
    if (avgConnections*2 >= number):
        avgConnections = int(number/2)
    if avgConnections <= 3:
        plusminus = 1
    else:
        plusminus = int(avgConnections/3)

    for m in range(number):
        numConnectDict[m] = 0
        personalConnectDict[m] = 0
    for i in range(number):
        numConnections = random.randint(
            avgConnections-plusminus, avgConnections+plusminus)
        #print("i : ", i, "conn : ", numConnections,)
        while True:
            link = random.randint(0, number-1)
            tot = 0
            for j in range(number):

                if numConnectDict[link] >= numConnections:
                    tot += 1
                    link = random.randint(0, number-1)
                else:
                    break
            if link != i:
                if numConnectDict[i] < numConnections:
                    if (link, i) not in greenLinks and (i, link) not in greenLinks:
                        greenLinks.append((i, link))
                        numConnectDict[i] = numConnectDict[i] + 1
                        personalConnectDict[i] = personalConnectDict[i] + 1
                        numConnectDict[link] = numConnectDict[link] + 1
                else:
                    break

        if personalConnectDict[i] <= 0:
            link = random.randint(0, number-1)
            while link == i:
                link = random.randint(0, number-1)
            greenLinks.append((i, link))
            numConnectDict[i] = numConnectDict[i] + 1
            personalConnectDict[i] = personalConnectDict[i] + 1
            numConnectDict[link] = numConnectDict[link] + 1
        #print("i : ", i, "conn both sides : ", numConnectDict[i])
        #print("i : ", i, "conn start: ", personalConnectDict[i])

    for i in range(number):
        for j in range(number):
            if (i, j) in greenLinks and (j, i) in greenLinks:
                #print("bhabah", i, j)
                if personalConnectDict[i] > 1:
                    personalConnectDict[i] -= 1
                    greenLinks.remove((i, j))
                if personalConnectDict[j] > 1:
                    greenLinks.remove((j, i))
                    personalConnectDict[j] -= 1

    greenLinks = list(dict.fromkeys(greenLinks))

    return greenLinks


def formatGreen(number, greenlinks, uMin, uMax):
    linksDict = {}
    for link in greenlinks:     # -1 here because in arrays we start counting at 0 but the given "network-2.csv" starts at 1
        try:
            linksDict[link[0]].append(link[1])
        except:
            linksDict[link[0]] = [link[1]]
    sort_keys = linksDict.items()
    sorted_links = sorted(sort_keys)
    # print(sorted_links)
    fixlist = []
    for i in range(number):
        fixlist.append(i)
    for link in sorted_links:
        fixlist.remove(link[0])
    for i in fixlist:
        sorted_links.append((i, []))
    sorted_links = sorted(sorted_links)
    # print(sorted_links)
    """for i in range(len(greenlinks)):
        if i == sorted_links[i][0]:
            continue
        else:
            sorted_links.append((i, []))
            sort_keys = linksDict.items()
            sorted_links = sorted(sort_keys)
    print(sorted_links)"""
    outGreen = []
    ngreen = 0
    for i in sorted_links:
        ngreen += 1
        if ngreen % 2 == 0:
            # uMin and uMax are min and max uncertainty
            uncertainRand = round(
                random.random()*(uMin*0.5)+random.random()*(uMax*0.5), 3)-0.5
            outGreen.append([i[1], uncertainRand, 0])
        else:
            # uMin and uMax are min and max uncertainty
            uncertainRand = round(
                random.random()*(uMin*0.5)+random.random()*(uMax*0.5), 3)+0.5
            outGreen.append([i[1], uncertainRand, 0])
    # print(outGreen)
    return outGreen


def findVoting(green):
    numVoting = 0
    numNotVoting = 0
    for n in green:
        val = n[1]
        if val < 0:
            numNotVoting += 1
        else:
            numVoting += 1
    return numVoting, numNotVoting


def plotGreen1(greenLinks, green, c):
    fig, axs = plt.subplots(1, 2, figsize=(9, 4))
    g = ig.Graph(totalGreen, greenLinks)
    arr = []
    for i in range(totalGreen):
        arr.append("v")
    g.vs["voting"] = arr
    for i in range(totalGreen-1):
        if green[i][1] > 0:
            g.vs[i]['voting'] = "v"
        else:
            g.vs[i]['voting'] = "n"
    g.vs[2]['color'] = "blue"
    color_dict = {"v": "blue", "n": "red", "u": "green"}
    ig.plot(
        g,
        target=axs[0],
        layout="circle",
        vertex_size=0.1,
        vertex_frame_width=2.0,
        vertex_frame_color=[color_dict[voting] for voting in g.vs["voting"]],
        vertex_color="green"
        # vertex_label_size=7.0
    )
    uncertaintiesX = [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -
                      0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    uQuantityY = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for n in green:
        val = round(n[1], 1)
        uQuantityY[uncertaintiesX.index(val)] += 1
    axs[1].plot(uncertaintiesX, uQuantityY, color=c)
    axs[1].set_title('Uncertainites')
    plt.show()


def plotGreen6(greenLinks, greenRound):
    fig, axs = plt.subplots(3, 2, figsize=(9, 7))
    gs = axs[0, 0].get_gridspec()
    for ax in axs[0:, 0]:
        ax.remove()
    axsbig = fig.add_subplot(gs[0:, 0])
    g = ig.Graph(totalGreen, greenLinks)
    arr = []
    for i in range(totalGreen):
        arr.append("v")
    g.vs["voting"] = arr
    colors = ["blue", "red", "green"]
    # print(greenRound[t])
    for i in range(totalGreen):
        if greenRound[2][i][1] > 0:
            g.vs[i]['voting'] = "v"
        else:
            g.vs[i]['voting'] = "n"
    color_dict = {"v": "blue", "n": "red", "u": "green"}
    ig.plot(
        g,
        target=axsbig,
        layout="circle",
        vertex_size=0.1,
        vertex_frame_width=2.0,
        vertex_frame_color=[color_dict[voting] for voting in g.vs["voting"]],
        vertex_color="green"
    )
    uncertaintiesX = [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -
                      0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    uQuantityY = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for t in range(len(greenRound)):
        for n in greenRound[t]:
            val = round(n[1], 1)
            uQuantityY[uncertaintiesX.index(val)] += 1
        axs[t, 1].plot(uncertaintiesX, uQuantityY, color=colors[t])
    axs[0, 1].set_title('Uncertainites')
    plt.show()


def GREENinteract():
    for node in greenNodes:
        for c in node[0]:
            unc_1 = node[1]
            unc_2 = greenNodes[c][1]
            if unc_1 < 0:
                unc_1 = -unc_1
            if unc_2 < 0:
                unc_2 = -unc_2
            if unc_1 == unc_2:
                continue
            if unc_1 > unc_2:
                change = (node[1]-greenNodes[c][1])/10
                greenNodes[c][1] = greenNodes[c][1] + change
            else:
                change = (-node[1]+greenNodes[c][1])/10
                node[1] = node[1] + change


def possibleInteract(green):
    canInteract = []
    numInteracts = 0
    for nodeID in range(len(green)):
        if (green[nodeID][2] == 0):
            canInteract.append(nodeID)
            numInteracts += 1
    return canInteract, numInteracts


def REDinteract(Power, totalGreen):
    global strongRed
    global FollowersLost
    #print("strongred", strongRed, strongBlue)
    canInteract, numInteracts = possibleInteract(
        greenNodes)  # Move this call to possible interactions
    #FollowersLost = 100 - int((numInteracts/totalGreen)*100)
    numVoting, numNotVoting = findVoting(greenNodes)
    if (numNotVoting/totalGreen*100) < 75:
        #print("Followers Lost : ", FollowersLost)
        if Power == 0:
            # losslist=[0,10,15,25,40]
            if FollowersLost < 30:
                SafeMoves = [4, 5]
                nextSafeMove = random.choice(SafeMoves)
                REDattack((nextSafeMove), canInteract)
            elif FollowersLost < 40:
                SafeMoves = [3, 4]
                nextSafeMove = random.choice(SafeMoves)
                REDattack((nextSafeMove), canInteract)
            elif FollowersLost < 60:
                SafeMoves = [1, 2, 3]
                nextSafeMove = random.choice(SafeMoves)
                REDattack((nextSafeMove), canInteract)
            elif FollowersLost < 80:
                SafeMoves = [1, 2]
                nextSafeMove = random.choice(SafeMoves)
                REDattack((nextSafeMove), canInteract)
            else:
                SafeMoves = [1]
                nextSafeMove = random.choice(SafeMoves)
                REDattack((nextSafeMove), canInteract)
            #print("Red attack : ", nextSafeMove)
        else:
            REDattack((Power), canInteract)
            #print("attck zero")
    else:
        SafeMoves = [2, 3]
        nextSafeMove = random.choice(SafeMoves)
        REDattack((nextSafeMove), canInteract)


def REDattack(power, canInteract):
    global EnergyLevel
    global FollowersLost
    global greenNodes
    global lastmoves
    #print("lastmoves :", lastmoves)
    EnergyLevel += 15

    strong_Red_Options = [0.1, 0.082, 0.15]   # ,0.87,1]
    strongRed = random.choice(strong_Red_Options)

    if (EnergyLevel > 100):
        EnergyLevel = 100
    for nodeID in range(len(greenNodes)):
        a = greenNodes[nodeID][2]
        if (a == 1):
            FollowersLost -= 1/len(greenNodes)*100
        if (a > 0):
            greenNodes[nodeID][2] -= 1

    #print("can interact", canInteract)
    for i in canInteract:
        if lastmoves.count(5) >= 3:
            lastmoves = [0, 0, 0, 0, 0]
            if greenNodes[i][1] < 0:
                greenNodes[i][1] = -(greenNodes[i][1])
            else:
                greenNodes[i][1] -= (strongRed*power)
                greenNodes[i][1] = round(greenNodes[i][1], 3)
            # print("popeye")
            continue
        elif greenNodes[i][1] < -0.70 and power > 3:
            greenNodes[i][1] -= (2*greenNodes[i][1])
            greenNodes[i][1] = round(greenNodes[i][1], 3)
        else:
            greenNodes[i][1] -= (strongRed*power)
            greenNodes[i][1] = round(greenNodes[i][1], 3)
        if (greenNodes[i][1] < -1):
            greenNodes[i][1] = -1
        if random.random() < power/10:
            #print("random :", random.random())
            greenNodes[i][2] = 2
            FollowersLost += 1/len(greenNodes)*100


def BLUEinteract(power, totalGreen):
    global gameover
    global EnergyLevel
    global GREY_Agents
    global costofattacks
    global strongBlue
    greyBool = False
    #print("Energy Level : ", EnergyLevel)

    if power == 0:
        if EnergyLevel == 100:  # and CertainityIsHigh and TimeIsAlmostUp:
            SafeMoves = [4, 5]
            nextSafeMove = random.choice(SafeMoves)
            BLUEattack(nextSafeMove)
        elif EnergyLevel > 80:
            SafeMoves = [3, 4, 5]
            nextSafeMove = random.choice(SafeMoves)
            BLUEattack(nextSafeMove)
        elif EnergyLevel > 50:
            SafeMoves = [2, 3, 4]
            nextSafeMove = random.choice(SafeMoves)
            BLUEattack(nextSafeMove)
        elif EnergyLevel > 30:
            SafeMoves = [1, 2, 3, 0]      # 0 is for grey agent helpline
            newSafeMoves = [3, 4, 5]        # only attacks permissable
            newSafeMove = random.choice(newSafeMoves)
            nextSafeMove = random.choice(SafeMoves)  # includes grey agent as 0
            if (nextSafeMove == 0 and len(GREY_Agents) != 0):
                GREYhelp()
                nextSafeMove = newSafeMove
                greyBool = True
                # print('grey')
            else:
                BLUEattack(nextSafeMove)
        elif EnergyLevel >= 15:
            SafeMoves = [1, 2, 0]           # 0 is for grey agent helpline
            newSafeMoves = [3, 4, 5]        # only attacks permissable
            newSafeMove = random.choice(newSafeMoves)
            nextSafeMove = random.choice(SafeMoves)  # includes grey agent as 0
            if (nextSafeMove == 0 and len(GREY_Agents) != 0):
                GREYhelp()
                nextSafeMove = newSafeMove
                greyBool = True
                # print('grey')
            else:
                BLUEattack(newSafeMove)
        else:
            SafeMoves = [1, 0]           # 0 is for grey agent helpline
            newSafeMoves = [3, 4, 5]        # only attacks permissable
            newSafeMove = random.choice(newSafeMoves)
            nextSafeMove = random.choice(SafeMoves)  # includes grey agent as 0
            if (nextSafeMove == 0 and len(GREY_Agents) != 0):
                GREYhelp()
                nextSafeMove = newSafeMove
                greyBool = True
                # print('grey')
            else:
                BLUEattack(newSafeMove)
        if (greyBool == False):
            EnergyLevel -= costofattacks[nextSafeMove-1]
    else:
        BLUEattack(power*0.8)
        if (greyBool == False):
            EnergyLevel -= costofattacks[power-1]


def BLUEattack(power):
    global greenNodes

    strong_Blue_Options = [0.07, 0.075, 0.082]  # ,0.87,1]
    strongBlue = random.choice(strong_Blue_Options)

    for green in greenNodes:

        green[1] = green[1] + ((strongBlue*power))
        green[1] = round(green[1], 3)
        if (green[1] > 1):
            green[1] = 1


def GREYhelp():
    global automatic
    global GREY_Agents
    #global totalGreen
    costofattacks = [10, 15, 25, 30, 40]

    greyRand = random.randint(1, len(GREY_Agents))
    greyMove = GREY_Agents.pop(greyRand-1)
    if (greyMove == 1):
        SafeMoves = [4, 5]
        nextSafeMove = random.choice(SafeMoves)
        BLUEattack(nextSafeMove)
    else:
        canInteract, numInteracts = possibleInteract(
            greenNodes)  # Move this call to possible interactions
        if automatic == False:
            print('Grey agent turned out to be a RedSpy ')
        SafeMoves = [1, 2, 3]
        nextSafeMove = random.choice(SafeMoves)
        # print(nextSafeMove)
        REDattack(nextSafeMove, canInteract)


def main():
    global automatic
    global EnergyLevel
    global totalGreen
    global GREY_Agents
    global greenNodes
    global costofattacks
    global gameover
    global strongRed
    global strongBlue
    global strongGrey
    global strongGreySpy
    global FollowersLost
    global lastmoves
    gameover = False
    costofattacks = [10, 15, 25, 30, 40]
    automatic = False
    while True:
        customGame = True
        playerInput = input(
            "How would you like to play? (Enter 'c' for a custom game or 'p' for a game with set parameters)\n")
        if playerInput.lower() == "p":
            customGame = False
            totalGreen = 10
            avgConnect = 2
            uncInterval = (-0.5, 0.5)
            greenLinks = createGreen(totalGreen, avgConnect)
            greenNodes = formatGreen(
                totalGreen, greenLinks, uncInterval[0], uncInterval[1])
            numGrey = 3
            greySpy = 1
            GREY_Agents = createGrey(numGrey, greySpy)
        elif playerInput.lower() != "c":
            break
        EnergyLevel = 100
        if customGame:
            while True:
                totalGreen = input(
                    "How many GREEN agents are there? (minimum 3)\n")
                try:
                    totalGreen = int(totalGreen)
                    if totalGreen >= 3:
                        break
                    else:
                        print("Green agents cannot be less than 3, try again")
                except ValueError:
                    print("Please enter a valid number of GREEN agents")
            while True:
                avgConnect = input(
                    "What is the average number of connections for each GREEN agent? (minimum 1)\n")
                try:
                    avgConnect = int(avgConnect)
                    if avgConnect >= 1:
                        break
                    else:
                        print("Average Connections cannot be less than 1, try again")
                except ValueError:
                    print(
                        "Please enter a valid number for average number of connections of GREEN agents")
            while True:
                uncInterval = str(
                    input("What is the uncertainty interval? E.g. (-0.5, 0.5)\n"))
                try:
                    if not uncInterval:
                        raise ValueError('empty string')
                    res = isinstance(uncInterval, tuple)
                    if str(res):
                        uncInterval = eval(uncInterval)
                        print(len(uncInterval))
                        if len(uncInterval) != 2:
                            print('tuple cannot be empty')
                            continue
                        if uncInterval[0] >= -1 and uncInterval[0] <= 1 or uncInterval[1] >= -1 and uncInterval[1] <= 1:
                            break
                        else:
                            print("Uncertainity values need to be between -1 and 1")
                    else:
                        raise ValueError('empty string')
                except ValueError and SyntaxError:
                    print(
                        "Please enter a valid format for uncertainty intervals and Uncertainity values need to be between -1 and 1")
            greenLinks = createGreen(totalGreen, avgConnect)
            greenNodes = formatGreen(
                totalGreen, greenLinks, uncInterval[0], uncInterval[1])
            while True:
                numGrey = input(
                    "How many GREY agents are there? (minimum 1)\n")
                try:
                    numGrey = int(numGrey)
                    if numGrey >= 1:
                        break
                    else:
                        print("Grey Agents cannot be less than 1, try again")
                except ValueError:
                    print("Please enter a valid number of GREY agents")
            while True:
                greySpy = input("How many GREY agents are SPIES?\n")
                try:
                    greySpy = int(greySpy)
                    if greySpy >= 0 and greySpy <= numGrey:
                        break
                    else:
                        print(
                            "Grey Spies cannot be less than 0 or more than the Grey Agents , try again")
                except ValueError:
                    print("Please enter a valid number of GREY SPIES")
            GREY_Agents = createGrey(numGrey, greySpy)
        while True:
            playerInput = input(
                "Who would you like to play as? (Enter 'b' to play as blue team or 'r' to play as red team or 'a' to run an automatic simulation of game)\n")
            try:
                if playerInput in 'aAbBrR' and len(playerInput) == 1:
                    break
                else:
                    print("Please enter a valid response")
            except ValueError:
                print("Please enter a valid response")
        if playerInput in 'bB':
            lastmoves = [0, 0, 0, 0, 0]
            # print(greenNodes)
            FollowersLost = 0
            gamecount = 0
            strongBlue = 40
            strongRed = 37
            strongGrey = 40
            strongGreySpy = 40
            # rounds that have been played
            while True:
                gamecount += 1
                if EnergyLevel <= 0:
                    numVoting, numNotVoting = findVoting(greenNodes)
                    if gamecount >= 10:
                        if numVoting > numNotVoting:
                            print("You WON Congratulations")
                            break
                        else:
                            print("Red WON Better Luck Next Time")
                            break
                    else:
                        print('YOU LOST AS YOU DID NOT LAST 10 ROUNDS/TURNS')
                        print('GAME OVER BLUE RAN OUT OF ENERGY')
                        break
                if gamecount == 20:
                    numVoting, numNotVoting = findVoting(greenNodes)
                    print("20 ROUNDS REACHED - GAME OVER")
                    if numVoting > numNotVoting:
                        print("You WON Congratulations")
                        break
                    else:
                        print("Red WON Better Luck Next Time")
                        break
                print("Player Energy Level: ", EnergyLevel)
                print("GREY agents remaining: ", len(GREY_Agents))
                #plotGreen1(greenLinks, greenNodes, 'black')
                # playerInput = input(
                #    "Enter a power level or 'G' to use a GREY Agent: \n 1 - 10 Energy \n 2 - 15 Energy \n 3 - 25 Energy \n 4 - 30 Energy \n 5 - 40 Energy \n 6 to use a GREY Agent\n")
                while True:
                    Blue_Power = input(
                        "Enter a power level or '6' to use a GREY Agent: \n 1 - 10 Energy \n 2 - 15 Energy \n 3 - 25 Energy \n 4 - 30 Energy \n 5 - 40 Energy \n 6 to use a GREY Agent\n")
                    try:
                        Blue_Power = int(Blue_Power)
                        if Blue_Power >= 0 and Blue_Power <= 6:
                            break
                        else:
                            print("Please enter a correct response")
                    except ValueError:
                        print("Please enter a correct response")

                if Blue_Power == 6:
                    GREYhelp()
                else:
                    BLUEinteract(Blue_Power, totalGreen)
                plt.close()

                greenBlue = eval(str(greenNodes))
                REDinteract(0, totalGreen)
                greenRed = eval(str(greenNodes))
                GREENinteract()
                greenGreen = eval(str(greenNodes))
                plotGreen6(greenLinks, [greenBlue, greenRed, greenGreen])
                numVoting, numNotVoting = findVoting(greenNodes)
                print("Number of People willing to Vote : ", numVoting)
                print("Number of People not willing to Vote : ", numNotVoting)
        elif playerInput in 'rR':
            lastmoves = [0, 0, 0, 0, 0]
            FollowersLost = 0
            gamecount = 0
            while True:
                gamecount += 1
                if EnergyLevel <= 0:
                    numVoting, numNotVoting = findVoting(greenNodes)
                    if gamecount >= 10:
                        if numVoting > numNotVoting:
                            print("Blue WON Better Luck Next Time")
                            break
                        else:
                            print("You WON Congratulations")
                            break
                    else:
                        print('YOU WON AS BLUE RAN OUT OF ENERGY')
                        print('GAME OVER NO ENERGY LEFT IN BLUE')
                        break
                if gamecount == 20:
                    numVoting, numNotVoting = findVoting(greenNodes)
                    print("GAME OVER")
                    if numVoting > numNotVoting:
                        print("Blue WON Better Luck Next Time")
                        break
                    else:
                        print("You WON Congratulations")
                        break
                canInteract, numInteracts = possibleInteract(greenNodes)
                print("Red can interact with ", int(
                    (numInteracts/totalGreen)*100), "% of the population")
                while True:
                    Red_Power = input(
                        "Enter a power level : \n 1 - Around 10% Followers Loss\n 2 - Around 20% Followers Loss \n 3 - Around 30% Followers Loss \n 4 - Around 40% Followers Loss \n 5 - Around 50% Followers Loss \n ")
                    try:
                        Red_Power = int(Red_Power)
                        if Red_Power >= 0 and Red_Power <= 5:
                            break
                        else:
                            print("Please enter a correct response")
                    except ValueError:
                        print("Please enter a correct response")
                plt.close()
                BLUEinteract(0, totalGreen)
                greenBlue = eval(str(greenNodes))
                REDinteract(Red_Power, totalGreen)
                lastmoves.pop(0)
                lastmoves.append(Red_Power)
                greenRed = eval(str(greenNodes))
                GREENinteract()
                greenGreen = eval(str(greenNodes))
                plotGreen6(greenLinks, [greenBlue, greenRed, greenGreen])
                numVoting, numNotVoting = findVoting(greenNodes)
                print("Number of People willing to Vote : ", numVoting)
                print("Number of People not willing to Vote : ", numNotVoting)
        elif playerInput in 'aA':
            automatic = True
            lastmoves = [0, 0, 0, 0, 0]
            Red_Wins = 0
            Blue_Wins = 0
            Draw = 0
            FollowersLost = 0
            gamecount = 0
            while True:
                playerInput = input(
                    "Enter no. of times you want the simulation to run (e.g. 10) (Maximum : 100): ")
                try:
                    playerInput = int(playerInput)
                    if playerInput > 0 and playerInput < 101:
                        break
                    else:
                        print("Please enter a correct response")
                except ValueError:
                    print("Please enter a correct response")
            if playerInput > 0 and playerInput < 101:
                cc = 0
                for i in range(playerInput):
                    FollowersLost = 0

                    EnergyLevel = 100
                    greenLinks = createGreen(totalGreen, avgConnect)
                    greenNodes = formatGreen(
                        totalGreen, greenLinks, uncInterval[0], uncInterval[1])
                    number = totalGreen
                    Voting = 0
                    NotVoting = 0

                    GREY_Agents = createGrey(numGrey, greySpy)
                    for i in range(20):
                        Options = [1, 2]
                        move = random.choice(Options)
                        if move == 1:
                            REDinteract(0, totalGreen)
                            greenRed = eval(str(greenNodes))
                            BLUEinteract(0, totalGreen)
                            greenBlue = eval(str(greenNodes))
                            GREENinteract()
                            greenGreen = eval(str(greenNodes))
                        elif move == 2:
                            BLUEinteract(0, totalGreen)
                            greenBlue = eval(str(greenNodes))
                            REDinteract(0, totalGreen)
                            greenRed = eval(str(greenNodes))
                            GREENinteract()
                            greenGreen = eval(str(greenNodes))
                        if gameover == True:
                            gameover == False
                            break
                    for n in greenNodes:
                        val = n[1]
                        if val < 0:
                            NotVoting += 1
                        else:
                            Voting += 1
                    if Voting == NotVoting:
                        Draw += 1
                    elif Voting > NotVoting:
                        Blue_Wins += 1
                    elif Voting < NotVoting:
                        Red_Wins += 1
                    numVoting, numNotVoting = findVoting(greenNodes)

                    try:
                        plotGreen6(
                            greenLinks, [greenBlue, greenRed, greenGreen])
                    except ValueError:
                        print("error")
                    cc += 1
                    print("Game No. ", cc, "-- VOTING : ", numVoting,
                          "-- NOT VOTING : ", numNotVoting)
                print("\nRed Won ", Red_Wins, " Games\n")
                print("Blue Won ", Blue_Wins, " Games\n")
                print("Draw ", Draw, " Games\n")


main()
