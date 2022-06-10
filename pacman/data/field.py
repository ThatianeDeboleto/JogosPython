import os
from random import randint


class GameEngine(object):

    def __init__(self):

        self.levelPelletRemaining = 0
        self.levelObjects = [[levelObject("empty") for j in range(32)] for i in range(28)]   # generate 28x32 empty objects
        self.movingObjectPacman = movingObject("Pacman")
        self.movingObjectGhosts = [movingObject("Ghost") for n in range(4)]

        self.levelObjectNamesBlocker = ["wall", "cage"]
        self.levelObjectNamesPassable = ["empty", "pellet", "powerup"]


    def levelGenerate(self, level):
        # set a directory for the resource file
        pathCurrentDir = os.path.dirname(__file__)  # current script directory
        pathRelDir = "../resource/level{}.txt".format(level)
        pathAbsDir = os.path.join(pathCurrentDir, pathRelDir)

        levelFile = open(pathAbsDir, encoding="utf-8")
        levelLineNo = 0

        # read line by line with readlines(), 'levelLine' temporarily save the string
        for levelLine in levelFile.readlines():

            levelLineSplit = list(levelLine) # split levelLine into characters

            # generate level objects
            for i in range(28):

                if levelLineSplit[i] == "_":    # passage
                    self.levelObjects[i][levelLineNo].name = "empty"
                elif levelLineSplit[i] == "#":  # wall
                    self.levelObjects[i][levelLineNo].name = "wall"
                elif levelLineSplit[i] == "$":  # ghost spawn point
                    self.levelObjects[i][levelLineNo].name = "cage"


                elif levelLineSplit[i] == ".":  # score pellet
                    self.levelObjects[i][levelLineNo].name = "pellet"

                    # checking how many pellets are in the level
                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        self.levelPelletRemaining += 1
                    else:
                        pass


                elif levelLineSplit[i] == "*":  # power pellet
                    self.levelObjects[i][levelLineNo].name = "powerup"

                    # checking how many pellets are in the level
                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        self.levelPelletRemaining += 1
                    else:
                        pass


                elif levelLineSplit[i] == "@":  # pacman
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # give the starting coordinate
                    self.movingObjectPacman.coordinateRel[0] = i
                    self.movingObjectPacman.coordinateRel[1] = levelLineNo
                    self.movingObjectPacman.coordinateAbs[0] = i * 4
                    self.movingObjectPacman.coordinateAbs[1] = levelLineNo * 4


                elif levelLineSplit[i] == "&":  # free ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].isCaged = False
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break   # break current loop (with generator 'n')


                elif levelLineSplit[i] == "%":  # caged ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break   # break current loop (with generator 'n')


            levelLineNo += 1 # indicate which line we are

        levelFile.close()


    def encounterFixed(self, x, y):     # rel coord.
        if self.levelObjects[x][y].name == "empty":
            result = "empty"

        elif self.levelObjects[x][y].name == "pellet":
            result = "pellet"

        elif self.levelObjects[x][y].name == "powerup":
            result = "powerup"
        
        return result

    
    def encounterMoving(self, x, y):    # abs coord.

        result = "alive"    # default return

        for i in range(4):  # check if pacman encountered ghost
            m = self.movingObjectGhosts[i].coordinateAbs[0] # ghost's x coord.
            n = self.movingObjectGhosts[i].coordinateAbs[1] # ghost's y coord.

            if self.movingObjectGhosts[i].isActive == True and self.movingObjectGhosts[i].isCaged == False:
                if (m-3 < x < m+3) and (n-3 < y < n+3):   # check x coord. and y coord. parallelly, this is little bit benign determine (we can use +-4)
                    result = "dead"
                else:
                    pass
            else:
                pass
        
        return result



    def loopFunction(self):
        self.movingObjectPacman.MoveNext(self)
        self.movingObjectPacman.MoveCurrent(self)

        for i in range(4):
            if self.movingObjectGhosts[i].isActive == True:
                self.movingObjectGhosts[i].dirNext = self.movingObjectGhosts[i].MoveNextGhost(self, self.movingObjectGhosts[i].dirCurrent)
                self.movingObjectGhosts[i].MoveNext(self)
                self.movingObjectGhosts[i].MoveCurrent(self)
            
            else:
                pass






class levelObject(object):

    def __init__(self, name):
        self.reset(name)

    def reset(self, name):
        self.name = name
        self.isDestroyed = False



class movingObject(object):

    def __init__(self, name):
        self.reset(name)


    def reset(self, name):
        self.name = name
        self.isActive = False       # check this object is an active ghost (not used for pacman)
        self.isCaged = True         # check this object is caged (only for ghost)
        self.dirCurrent = "Left"    # current direction, if cannot move w/ dirNext, the object will proceed this direction
        self.dirNext = "Left"       # the object will move this direction if it can
        self.dirOpposite = "Right"  # opposite direction to current direction, used for ghost movement determine
        self.dirEdgePassed = False  # check the object passed one of field edges
        self.coordinateRel = [0, 0] # Relative Coordinate, check can the object move given direction
        self.coordinateAbs = [0, 0] # Absolute Coordinate, use for widget(image) and object encounters


    def MoveNextGhost(self, GameEngine, dirCur):
        ## this function will determine ghost's direction
        # if ghost reaches a grid coordinate, this will check all directions from the ghost's current location
        # we should get DOF here and will determine how we manage ghost's direction
        # DOF == 1 ... opposite direction
        # DOF == 2 ... current direction
        # DOF == 3 ... random direction (except opposite dir)
        # DOF == 4 ... random direction (except opposite dir)

        if self.isCaged == True:    # if ghost is caged, prevent the movement
            pass

        elif self.coordinateAbs[0] % 4 != 0: # if the object is moving, prevent to change its direction
            pass

        elif self.coordinateAbs[1] % 4 != 0: # if the object is moving, prevent to change its direction
            pass
        
        else:
            dirIndex = ['Left', 'Right', 'Up', 'Down'] # [0]: Left, [1]: Right, [2]: Up, [3]: Down
            dirAvailable = []
            dirDOF = 0

            # find the opposite direction
            if dirCur == 'Left':
                self.dirOpposite = 'Right'
            elif dirCur == 'Right':
                self.dirOpposite = 'Left'
            elif dirCur == 'Up':
                self.dirOpposite = 'Down'
            elif dirCur == 'Down':
                self.dirOpposite = 'Up'
            else: # dirCur == 'Stop'
                pass

            # checking all directions
            try:
                for i in range(4):

                    if i == 0:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject on the left
                    elif i == 1:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]] # levelObject on the right
                    elif i == 2:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1] # levelObject on the up
                    elif i == 3:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1] # levelObject on the down          

                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        dirDOF += 1
                        dirAvailable.append(dirIndex[i])    # append available direction to the list
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass

            except IndexError:  # in case of edge teleport
                dirDOF = 2
                dirAvailable.append(dirCur)
            

            try:
                if dirDOF == 1: # to opposite direction, in this case, dirAvailable only have one item (which is opposite dir)
                    return dirAvailable[0]  # this might not use dirOpp as if the object is stopped, dirOpp is not binded properly
                
                elif dirDOF == 2: # advance toward current direction
                    if dirCur in dirAvailable:  # straight
                        return dirCur
                    elif dirCur == 'Stop':  # somehow this object stopped at straight way
                        return dirAvailable[0]
                    else:   # curved
                        dirAvailable.remove(self.dirOpposite)
                        return dirAvailable[0]


                elif dirDOF == 3 or dirDOF == 4:
                    if dirCur == 'Stop':
                        randNo = randint(0, dirDOF-1)   # generate a random number, selection of degree of freedom
                        return dirAvailable[randNo]
                    else:
                        dirAvailable.remove(self.dirOpposite) # except the opposite direction
                        randNo = randint(0, dirDOF-2)   # generate a random number, selection of degree of freedom (except the opposite dir)
                        return dirAvailable[randNo]
            

            except ValueError:  # prevent the first loop error (default values would cause ValueError)
                pass



    def MoveNext(self, GameEngine):
        ## this function will determine pacman can move with given direction or not

        if self.dirNext == self.dirCurrent: # in this case, no action is required
            pass
        
        elif self.coordinateAbs[0] % 4 != 0: # if the object is moving, prevent to change its direction
            pass

        elif self.coordinateAbs[1] % 4 != 0: # if the object is moving, prevent to change its direction
            pass

        else:
            if self.dirNext == "Left":  # check the direction first

                if self.coordinateRel[0] == 0: # at left edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Left"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject placed left of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Left"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass
                

            elif self.dirNext == "Right":

                if self.coordinateRel[0] == 27: # at right edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Right"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]] # levelObject placed right of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Right"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Down":

                if self.coordinateRel[1] == 31: # at bottom edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Down"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1] # levelObject placed down of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Down"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Up":

                if self.coordinateRel[1] == 0: # at top edge, allow to change direction without checking (prevent index error)
                    self.dirCurrent = "Up"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1] # levelObject placed up of this object

                    # check the levelObject and allow movingObject to change its current direction
                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Up"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass

        
    
    def MoveCurrent(self, GameEngine):

        if self.dirCurrent == "Left":

            if self.coordinateAbs[0] == 0: # at left edge, move to right edge
                self.coordinateAbs[0] = 27*4 + 3
                self.coordinateRel[0] = 28
                self.dirEdgePassed = True
            
            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject placed left of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[0] -= 1 # adjust current coordinate
                    if self.coordinateAbs[0] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] -= 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Right":

            if self.coordinateAbs[0] == 27*4:  # at right edge, move to left edge
                self.coordinateAbs[0] = -3
                self.coordinateRel[0] = -1
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]] # levelObject placed right of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[0] += 1  # adjust current coordinate
                    if self.coordinateAbs[0] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] += 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Down":

            if self.coordinateAbs[1] == 31*4:  # at bottom edge, move to top edge
                self.coordinateAbs[1] = -3
                self.coordinateRel[1] = -1
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1] # levelObject placed down of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[1] += 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] += 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Up":

            if self.coordinateAbs[1] == 0:  # at top edge, move to bottom edge
                self.coordinateAbs[1] = 31*4 + 3
                self.coordinateRel[1] = 32
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1] # levelObject placed up of this object
                # check the levelObject and allow movingObject to move its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[1] -= 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 4 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] -= 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Stop":
            pass


gameEngine = GameEngine()