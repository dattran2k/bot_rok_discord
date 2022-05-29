scientistGlo = []
dukeGlo = []
architectGlo = []
judgeGlo = []
import logging
logging.basicConfig(level=logging.INFO)
class Data():
    def __init__(self,x = 0,y = 0,title = '',timeRequest = 0,timeGiveTitle = 0,time = 0):
        self.x = x
        self.y = y
        self.title = title
        self.timeRequest = timeRequest
        self.timeGiveTitle = timeGiveTitle
        self.time = time
    
    def getScient():
        print(scientistGlo)
        return scientistGlo
    def getDuke():
        return dukeGlo
    def getArchitect():
        return architectGlo
    def getJudge():
        return judgeGlo

    def addScient(obj):
        return scientistGlo.append(obj)
    def addDuke(obj):
        return dukeGlo.append(obj)
    def addArchitect(obj):
        return architectGlo.append(obj)
    def addJudge(obj):
        return judgeGlo.append(obj)
    
    def removeScient(obj):
        return scientistGlo.remove(obj)
    def removeDuke(obj):
        return dukeGlo.remove(obj)
    def removeArchitect(obj):
        return architectGlo.remove(obj)
    def removeJudge(obj):
        return judgeGlo.remove(obj)

    def updateScient(index,obj):
        scientistGlo[index] = obj
    def updateDuke(index,obj):
        dukeGlo[index] = obj
    def updateArchitect(index,obj):
        architectGlo[index] = obj
    def updateJudge(index,obj):
        judgeGlo[index] = obj