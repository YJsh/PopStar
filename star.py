# -*- coding: gbk -*-
import random
from data import level_score_data as LSD
from const import *

class Star (object):
    def __init__ (self, color=None, position=None):
        super(Star, self).__init__()
        self.state = STAR_STATE_INIT
        self.color = color
        self.position = position

    def setState (self, state):
        self.state = state

    def getState (self):
        return self.state

    def setColor (self, color):
        if len(color) != 3:
            return
        self.color = color
        print self.color

    def getColor (self):
        if self.color == (255,255,255):
            print self.color
        return self.color if self.color != None else (0, 0, 0)

    def setPosition (self, position):
        if len(position) != 2:
            return
        self.position = position

    def getPosition (self):
        return self.position if self.position != None else (0, 0)

class StarArray (list):
    def __init__ (self):
        super(StarArray, self).__init__()
        self.starNum = 0
        self.level = 0
        self.score = 0
        self.initStars()
        self.isFinish = False

    def initStars (self):
        self.checkedStars = []
        self.activatedStars = []
        self.delStars = {}
        self.clear()
        for i in xrange(STAR_NUM):
            starList = []
            for j in xrange(STAR_NUM):
                color = random.choice(STAR_COLOR)
                star = Star(color, (i,j))
                starList.append(star)
            self.append(starList)
        self.level += 1
        self.starNum = STAR_NUM ** 2

    def clear (self):
        while self:
            self.pop()
    def clearActivatedStars (self):
        for star in self.activatedStars:
            star.setState(STAR_STATE_INIT)
            self.checkedStars.append(star)
        self.activatedStars = []

    def isChecked (self, star):
        return star in self.checkedStars

    def activateStars (self, star):
        print "activateStars", star.position
        color = star.color
        starQueue = [star]
        self.checkedStars.append(star)
        while starQueue:
            checkedStar = starQueue.pop(0)
            if checkedStar.color == color:
                checkedStar.state = STAR_STATE_ACTIVATED
                self.activatedStars.append(checkedStar)
                x, y = checkedStar.position
                if y > 0:
                    nextStar = self[x][y-1]
                    if not self.isChecked(nextStar):
                        starQueue.append(nextStar)
                        self.checkedStars.append(nextStar)
                if y < len(self[x]) - 1:
                    nextStar = self[x][y+1]
                    if not self.isChecked(nextStar):
                        starQueue.append(nextStar)
                        self.checkedStars.append(nextStar)
                if x > 0 and y < len(self[x-1]):
                    nextStar = self[x-1][y]
                    if not self.isChecked(nextStar):
                        starQueue.append(nextStar)
                        self.checkedStars.append(nextStar)
                if x < len(self) - 1 and y < len(self[x+1]):
                    nextStar = self[x+1][y]
                    if not self.isChecked(nextStar):
                        starQueue.append(nextStar)
                        self.checkedStars.append(nextStar)
        if len(self.activatedStars) == 1:
            self.activatedStars[0].state = STAR_STATE_INIT
            self.activatedStars = []
        self.checkedStars = []
        x = []
        for star in self.activatedStars:
            x.append(star.position)
        print "activate pos", x

    def popStar (self):
        print "popStar"
        num = len(self.activatedStars)
        self.score += 5 * num ** 2
        self.starNum -= num
        for star in self.activatedStars:
            x, y = star.position
            print x, y
            if not self.delStars.get(x):
                self.delStars[x] = [y]
            else:
                self.delStars[x].append(y)
        print "delStars", self.delStars

        index = 0
        offsetX, offsetY = 0, 0
        for index in xrange(len(self)):
            delStarList = self.delStars.get(index, [])
            if delStarList == [] and offsetX == 0:
                continue
            starList = self[index]
            offsetY = len(delStarList)
            if len(starList) == offsetY:
                offsetX += 1
                print offsetX, index
                self[index] = None
                continue
            delPosList = sorted(delStarList)
            for pos in sorted(xrange(len(starList)), reverse=True):
                star = starList[pos]
                if offsetX == 0 and offsetY == 0:
                    break
                print delPosList
                if len(delPosList) > 0 and star.position[1] == delPosList[-1]:
                    print star.position[1]

                    offsetY -= 1
                    delPosList.pop()
                    print "listPos", delPosList
                    continue
                star.position = (star.position[0] - offsetX, star.position[1] - offsetY)
            for pos in sorted(delStarList, reverse=True):
                starList.pop(pos)

        for i in xrange(offsetX):
            self.remove(None)
        self.delStars = {}
        if self.checkFinish():
            self.score += max(0, 2000 - 20 * self.starNum ** 2)
            if self.checkScore():
                self.initStars()
            else:
                self.isFinish = True

        for l in self:
            x = []
            for s in l:
                x.append(s.position)
            print x

    def checkFinish (self):
        isFinish = True
        if self.starNum == 0:
            return isFinish

        for starList in self:
            for star in starList:
                x, y = star.position
                if y > 0:
                    nextStar = self[x][y-1]
                    if nextStar.color == star.color:
                        isFinish = False
                        break
                if y < len(self[x]) - 1:
                    nextStar = self[x][y+1]
                    if nextStar.color == star.color:
                        isFinish = False
                        break
                if x > 0 and y < len(self[x-1]):
                    nextStar = self[x-1][y]
                    if nextStar.color == star.color:
                        isFinish = False
                        break
                if x < len(self) - 1 and y < len(self[x+1]):
                    nextStar = self[x+1][y]
                    if nextStar.color == star.color:
                        isFinish = False
                        break
            if not isFinish:
                break
        return isFinish

    def checkScore (self):
        levelScore = LSD.data.get(self.level, 999999)
        if levelScore < self.score:
            return True
        return False
