from tkinter import Tk, Label, Entry, Button, PhotoImage, messagebox, END, Canvas
from threading import Timer
from data import field
import os, pygame


class MainEngine(object):

    def __init__(self):


        self.root = Tk()
        self.root.title("Pac-Man")
        self.root.geometry("480x640")
        self.root.resizable(0, 0)

        self.currentLv = 1
        self.isLevelGenerated = False
        self.isPlaying = False
        self.statusStartingTimer = 0
        self.statusDeadTimer = 0
        self.statusFinishTimer = 0
        self.statusScore = 0
        self.statusLife = 2             # life

        # call the next phase of initialization: loading resources
        self.__initResource()


    def __initResource(self):
        ## read the sprite files
        # all sprites will saved in this dictionary
        self.wSprites = {
            'getready': PhotoImage(file="resource/sprite_get_ready.png"),
            'gameover': PhotoImage(file="resource/sprite_game_over.png"),
            'wall': PhotoImage(file="resource/sprite_wall.png"),
            'cage': PhotoImage(file="resource/sprite_cage.png"),
            'pellet': PhotoImage(file="resource/sprite_pellet.png")
        }

        # bind sprites for moving objects
        for i in range(4):
            # pacman: pacman(direction)(index)
            if i == 3:
                pass
            else:
                self.wSprites['pacmanL{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_left{}.png".format(i+1))
                self.wSprites['pacmanR{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_right{}.png".format(i+1))
                self.wSprites['pacmanU{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_up{}.png".format(i+1))
                self.wSprites['pacmanD{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_down{}.png".format(i+1))
            # ghosts: ghost(index1)(direction)(index2)
            self.wSprites['ghost{}L1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_left1.png".format(i+1))
            self.wSprites['ghost{}L2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_left2.png".format(i+1))
            self.wSprites['ghost{}R1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_right1.png".format(i+1))
            self.wSprites['ghost{}R2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_right2.png".format(i+1))
            self.wSprites['ghost{}U1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_up1.png".format(i+1))
            self.wSprites['ghost{}U2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_up2.png".format(i+1))
            self.wSprites['ghost{}D1'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_down1.png".format(i+1))
            self.wSprites['ghost{}D2'.format(i+1)] = PhotoImage(file="resource/sprite_ghost_{}_down2.png".format(i+1))

        for i in range(11):
            self.wSprites['pacmanDeath{}'.format(i+1)] = PhotoImage(file="resource/sprite_pacman_death{}.png".format(i+1))


        self.wSounds = {
            'chomp1': pygame.mixer.Sound(file="resource/sound_chomp1.wav"),
            'chomp2': pygame.mixer.Sound(file="resource/sound_chomp2.wav")
        }

        # call the next phase of initialization: generate widgets
        self.__initWidgets()


    def __initWidgets(self):
        # initialize widgets for level selection
        self.wLvLabel = Label(self.root, text="Select the level.")
        self.wLvEntry = Entry(self.root)
        self.wLvBtn = Button(self.root, text="Select", command=self.lvSelect, width=5, height=1)

        # initialize widgets for the game
        self.wGameLabelScore = Label(self.root, text=("Score: " + str(self.statusScore)))
        self.wGameLabelLife = Label(self.root, text=("Life: " + str(self.statusLife)))
        self.wGameCanv = Canvas(width=480, height=600)
        self.wGameCanvLabelGetReady = self.wGameCanv.create_image(240,326,image=None)
        self.wGameCanvLabelGameOver = self.wGameCanv.create_image(240,327,image=None)  
        self.wGameCanvObjects = [[self.wGameCanv.create_image(0,0,image=None) for j in range(32)] for i in range(28)]
        self.wGameCanv.config(background="black")
        self.wGameCanvMovingObjects = [self.wGameCanv.create_image(0,0,image=None) for n in range(5)] # 0: pacman, 1-4: ghosts

        # key binds for the game control
        self.root.bind('<Left>', self.inputResponseLeft)
        self.root.bind('<Right>', self.inputResponseRight)
        self.root.bind('<Up>', self.inputResponseUp)
        self.root.bind('<Down>', self.inputResponseDown)
        self.root.bind('<Escape>', self.inputResponseEsc)
        self.root.bind('<Return>', self.inputResponseReturn)

        # call the next phase of initialization: level selection
        self.__initLevelSelect()


    def __initLevelSelect(self):
        ## level selection, showing all relevant widgets
        self.wLvLabel.pack()
        self.wLvEntry.pack()
        self.wLvBtn.pack()

        # execute the game
        self.root.mainloop()


    def lvSelect(self):
        try:
            self.__initLevelOnce(self.wLvEntry.get())

        except ValueError:
            self.wLvEntry.delete(0, END)  # clear the text box
            messagebox.showinfo("Error!", "Enter a valid level.")

        except FileNotFoundError:
            self.wLvEntry.delete(0, END)  # clear the text box
            messagebox.showinfo("Error!", "Enter a valid level.")


    def __initLevelOnce(self, level):
        ## this function will be called only once

        self.__initLevel(level)

        # removing level selection features
        self.wLvLabel.destroy()
        self.wLvEntry.destroy()
        self.wLvBtn.destroy()
        # place the canvas and set isPlaying True
        self.wGameCanv.place(x=0, y=30)
        self.wGameLabelScore.place(x=10, y=5)
        self.wGameLabelLife.place(x=420, y=5)




    def __initLevel(self, level):

        self.currentLv = int(level)
        field.gameEngine.levelGenerate(level)   # generate selected/passed level

        # check the name of the object and bind the sprite, adjust their coordinate
        for j in range(32):
            for i in range(28):

                if field.gameEngine.levelObjects[i][j].name == "empty":
                    pass
                elif field.gameEngine.levelObjects[i][j].name == "wall":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'], state='normal')
                    self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3+i*17+8, 30+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "cage":
                    self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['cage'], state='normal')
                    self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3+i*17+8, 30+j*17+8)
                elif field.gameEngine.levelObjects[i][j].name == "pellet":
                    if field.gameEngine.levelObjects[i][j].isDestroyed == False:
                        self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['pellet'], state='normal')
                        self.wGameCanv.coords(self.wGameCanvObjects[i][j], 3+i*17+8, 30+j*17+8)
                    else:
                        pass

        # bind the sprite and give it current coord. for pacman
        self.wGameCanv.coords(self.wGameCanvMovingObjects[0], 
                            3+field.gameEngine.movingObjectPacman.coordinateRel[0]*17+8,
                            30+field.gameEngine.movingObjectPacman.coordinateRel[1]*17+8)
        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL1'], state='normal')

        # bind the sprite give them current coord. for ghosts
        for i in range(4):
            if field.gameEngine.movingObjectGhosts[i].isActive == True:
                self.wGameCanv.coords(self.wGameCanvMovingObjects[i+1],
                                    3+field.gameEngine.movingObjectGhosts[i].coordinateRel[0]*17+8,
                                    30+field.gameEngine.movingObjectGhosts[i].coordinateRel[1]*17+8)
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[i+1], image=self.wSprites['ghost{}L1'.format(i+1)], state='normal')


        # advance to next phase: get ready!
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resource/sound_intro.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)
        self.isLevelGenerated = True
        self.timerReady = PerpetualTimer(0.55, self.__initLevelStarting)
        self.timerReady.start()


    def inputResponseLeft(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Left"

    def inputResponseRight(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Right"

    def inputResponseUp(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Up"

    def inputResponseDown(self, event):
        field.gameEngine.movingObjectPacman.dirNext = "Down"

    def inputResponseEsc(self, event):
        self.timerLoop.stop()
        messagebox.showinfo("Game Over!", "You hit the escape key!")

    def inputResponseReturn(self, event):
        # skip feature
        if self.isLevelGenerated == True and self.isPlaying == False:
            self.gameStartingTrigger()
        else:
            pass



    def __initLevelStarting(self):
        self.statusStartingTimer += 1   # countdown timer for this function

        # bind the sprite for the widget
        self.wGameCanv.itemconfig(self.wGameCanvLabelGetReady, image=self.wSprites['getready'])

        if self.statusStartingTimer < 8:
            # blinking function
            if self.statusStartingTimer % 2 == 1:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='normal')
            else:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='hidden')

        else:   # after 8 loop, the main game will be started with loopFunction
            self.gameStartingTrigger()


    def gameStartingTrigger(self):
        ## stop to print out 'get ready' and start the game
        self.timerReady.stop()
        self.wGameCanv.itemconfigure(self.wGameCanvLabelGetReady, state='hidden')
        self.statusStartingTimer = 0
        self.isPlaying = True
        field.gameEngine.movingObjectPacman.dirNext = "Left"

        # ghost sound as music
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resource/sound_ghost.ogg")
        pygame.mixer.music.play(-1)

        self.timerLoop = PerpetualTimer(0.045, self.loopFunction)
        self.timerLoop.start()


    def loopFunction(self):

        field.gameEngine.loopFunction()

        coordGhosts = {}

        for i in range(4):
            coordGhosts['RelG{}'.format(i+1)] = field.gameEngine.movingObjectGhosts[i].coordinateRel    # ghosts relative coordinate
            coordGhosts['AbsG{}'.format(i+1)] = field.gameEngine.movingObjectGhosts[i].coordinateAbs    # ghosts absolute coordinate

        self.spritePacman(field.gameEngine.movingObjectPacman.coordinateRel, field.gameEngine.movingObjectPacman.coordinateAbs)
        self.spriteGhost(coordGhosts)
        self.encounterEvent(field.gameEngine.movingObjectPacman.coordinateRel, field.gameEngine.movingObjectPacman.coordinateAbs)




    def spritePacman(self, coordRelP, coordAbsP):
        ## pacman sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        if field.gameEngine.movingObjectPacman.dirCurrent == "Left":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 17*27+17, 0)    # notice this will move the sprite 17*27+17 (not 17*27+12) as the sprite will move once again below
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[0] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
            elif coordAbsP[0] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL3'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
            elif coordAbsP[0] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -4, 0)
            elif coordAbsP[0] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanL1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -5, 0)


        elif field.gameEngine.movingObjectPacman.dirCurrent == "Right":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], -(17*27+17), 0)
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[0] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
            elif coordAbsP[0] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR3'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
            elif coordAbsP[0] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 4, 0)
            elif coordAbsP[0] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanR1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 5, 0)


        elif field.gameEngine.movingObjectPacman.dirCurrent == "Up":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 17*31+17)
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[1] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
            elif coordAbsP[1] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU3'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
            elif coordAbsP[1] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -4)
            elif coordAbsP[1] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanU1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -5)


        elif field.gameEngine.movingObjectPacman.dirCurrent == "Down":

            # check the object passed field edges
            if field.gameEngine.movingObjectPacman.dirEdgePassed == True:
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, -(17*31+17))
                field.gameEngine.movingObjectPacman.dirEdgePassed = False
            else:
                pass

            if coordAbsP[1] % 4 == 0:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
            elif coordAbsP[1] % 4 == 1:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD3'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
            elif coordAbsP[1] % 4 == 2:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD2'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 4)
            elif coordAbsP[1] % 4 == 3:
                self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0], image=self.wSprites['pacmanD1'])
                self.wGameCanv.move(self.wGameCanvMovingObjects[0], 0, 5)


    def spriteGhost(self, coordGhosts):
        ## ghosts sprite feature
        # this will adjust the coordinate of the sprite and make them animated, based on their absoluteCoord.
        for ghostNo in range(4):
            if field.gameEngine.movingObjectGhosts[ghostNo].isActive == True:   # only active ghost will be shown
                if field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Left":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 17*27+17, 0)
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}L2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -5, 0)


                elif field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Right":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], -(17*27+17), 0)
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 4, 0)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][0] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}R2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 5, 0)


                elif field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Up":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 17*31+17)
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}U2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -5)


                elif field.gameEngine.movingObjectGhosts[ghostNo].dirCurrent == "Down":

                    # check the object passed field edges
                    if field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed == True:
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, -(17*31+17))
                        field.gameEngine.movingObjectGhosts[ghostNo].dirEdgePassed = False
                    else:
                        pass

                    if coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 0:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 1:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D1'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 2:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 4)
                    elif coordGhosts['AbsG{}'.format(ghostNo+1)][1] % 4 == 3:
                        self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[ghostNo+1], image=self.wSprites['ghost{}D2'.format(ghostNo+1)])
                        self.wGameCanv.move(self.wGameCanvMovingObjects[ghostNo+1], 0, 5)
            
            else:   # inactive ghost
                pass


    def encounterEvent(self, coordRelP, coordAbsP):
        ## encounter features

        encounterMov = field.gameEngine.encounterMoving(coordAbsP[0], coordAbsP[1]) # call encounterEvent for moving objects

        if encounterMov == 'dead':
            self.encounterEventDead()

        else:
            pass

        # check the object reaches grid coordinate
        if coordAbsP[0] % 4 == 0 and coordAbsP[1] % 4 == 0:
            encounterFix = field.gameEngine.encounterFixed(coordRelP[0], coordRelP[1]) # call encounterEvent function

            if encounterFix == "empty":
                pass
            elif encounterFix == "pellet":
                if field.gameEngine.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed == False:  # check the pellet is alive
                    field.gameEngine.levelObjects[coordRelP[0]][coordRelP[1]].isDestroyed = True # destroy the pellet
                    self.wGameCanv.itemconfigure(self.wGameCanvObjects[coordRelP[0]][coordRelP[1]], state='hidden') # remove from the canvas

                    # play the sound (wa, ka, wa, ka, ...)
                    if self.statusScore % 20 == 0:
                        self.wSounds['chomp1'].play(loops=0)
                    else:
                        self.wSounds['chomp2'].play(loops=0)

                    self.statusScore += 10 # adjust the score
                    self.wGameLabelScore.configure(text=("Score: " + str(self.statusScore))) # showing on the board
                    field.gameEngine.levelPelletRemaining -= 1 # adjust the remaining pellet numbers

                    if field.gameEngine.levelPelletRemaining == 0:
                        self.encounterEventLevelClear() # level clear
                    else:
                        pass


                else:   # the pellet is already taken
                    pass

        else: # pacman is not on grid coordinate
            pass


    def encounterEventLevelClear(self):
        # pause the game
        pygame.mixer.music.stop()
        self.timerLoop.stop()
        self.isPlaying = False

        for i in range(5):  # hide the moving objects' sprite
            self.wGameCanv.itemconfigure(self.wGameCanvMovingObjects[i], state='hidden')

        self.timerClear = PerpetualTimer(0.4, self.encounterEventLevelClearLoop)
        self.timerClear.start()


    def encounterEventLevelClearLoop(self):
        self.statusFinishTimer += 1   # countdown timer for this function

        if self.statusFinishTimer < 9:
            # wall blinking function
            if self.statusFinishTimer % 2 == 1:
                self.wSprites.update({'wall': PhotoImage(file="resource/sprite_wall2.png")})                
                for j in range(32):
                    for i in range(28):
                        if field.gameEngine.levelObjects[i][j].name == "wall":
                            self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'])
                        else:
                            pass
            else:
                self.wSprites.update({'wall': PhotoImage(file="resource/sprite_wall.png")})
                for j in range(32):
                    for i in range(28):
                        if field.gameEngine.levelObjects[i][j].name == "wall":
                            self.wGameCanv.itemconfig(self.wGameCanvObjects[i][j], image=self.wSprites['wall'])
                        else:
                            pass

        else:   # after 11 loop, the level clear process will be continued
            self.encounterEventLevelClearFinish()


    def encounterEventLevelClearFinish(self):
        self.timerClear.stop()
        self.statusFinishTimer = 0

        # reset all values and hide the sprite (or level generate process will be shown)
        for j in range(32):
            for i in range(28):
                field.gameEngine.levelObjects[i][j].reset('')
                #self.wGameCanv.itemconfigure(self.wGameCanvObjects[i][j], state='hidden')

        field.gameEngine.movingObjectPacman.reset('Pacman')

        for n in range(4):
            field.gameEngine.movingObjectGhosts[n].reset('Ghost')
        
        self.currentLv += 1
        self.isLevelGenerated = False
        self.__initLevel(self.currentLv)



    def encounterEventDead(self):

        self.statusLife -= 1    # subtract remaining life

        if self.statusLife >= 0:
            self.wGameLabelLife.configure(text=("Life: " + str(self.statusLife))) # showing on the board
        else:   # prevent showing minus life (will be game over anyway)
            pass

        # pause the game
        self.isPlaying = False
        pygame.mixer.music.stop()
        self.timerLoop.stop()

        # call the death loop
        self.timerDeath = PerpetualTimer(0.10, self.encounterEventDeadLoop)
        self.timerDeath.start()


    def encounterEventDeadLoop(self):

        self.statusDeadTimer += 1   # countdown timer for this function

        if self.statusDeadTimer <= 5:   # waiting for a while
            pass

        elif self.statusDeadTimer == 6:
            # sound effect
            pygame.mixer.music.load("resource/sound_death.mp3")
            pygame.mixer.music.play(loops=0, start=0.0)
            for i in range(4):  # hide the ghost sprite and initialize their status
                self.wGameCanv.itemconfigure(self.wGameCanvMovingObjects[i+1], state='hidden')
                field.gameEngine.movingObjectGhosts[i].isActive = False
                field.gameEngine.movingObjectGhosts[i].isCaged = True
        
        elif 6 < self.statusDeadTimer <= 17:    # animate the death sprite
            self.wGameCanv.itemconfig(self.wGameCanvMovingObjects[0],
                                        image=self.wSprites['pacmanDeath{}'.format(self.statusDeadTimer-6)])

        elif self.statusDeadTimer == 18:    # blink!
            self.wGameCanv.itemconfigure(self.wGameCanvMovingObjects[0], state='hidden')

        elif 18 < self.statusDeadTimer <= 22:   # waiting for a while
            pass

        else:
            self.encounterEventDeadRestart()


    def encounterEventDeadRestart(self):
        ## stop the death event and restart the game
        if self.statusLife >= 0:
            self.statusDeadTimer = 0    # reset the countdown timer
            self.timerDeath.stop()      # stopping the timer for death event
            self.isPlaying = False      # isPlaying flag check
            field.gameEngine.levelPelletRemaining = 0   # Pellet count reset (will be re-counted in __initLevel)
            self.__initLevel(self.currentLv)
        
        else:   # game over
            self.statusDeadTimer = 0
            self.timerDeath.stop()
            self.gameOverTimer = PerpetualTimer(0.55, self.encounterEventDeadGameOver)
            self.gameOverTimer.start()



    def encounterEventDeadGameOver(self):
        self.statusDeadTimer += 1
        self.wGameCanv.itemconfig(self.wGameCanvLabelGameOver, image=self.wSprites['gameover'])

        if self.statusDeadTimer < 8:
            # blinking function
            if self.statusDeadTimer % 2 == 1:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGameOver, state='normal')
            else:
                self.wGameCanv.itemconfigure(self.wGameCanvLabelGameOver, state='hidden')

        else:   # after 8 loop, the game is completely finished
            self.gameOverTimer.stop()




class PerpetualTimer(object):
    
    def __init__(self, interval, function, *args):
        self.thread = None
        self.interval = interval
        self.function = function
        self.args = args
        self.isRunning = False

    
    def _handleFunction(self):
        self.isRunning = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.isRunning:
            self.thread = Timer(self.interval, self._handleFunction)
            self.thread.start()
            self.isRunning = True

    def stop(self):
            self.thread.cancel()
            self.isRunning = False


# initialize pygame for sound effects
pygame.mixer.init(22050, -16, 2, 64)
pygame.init()

mainEngine = MainEngine()