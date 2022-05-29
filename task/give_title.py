from requests import post
from data.data_list import Data
from task.task import Task
import common.constants
from utils import Utils
from filepath.file_relative_paths import ImagePathAndProps
posfind = common.constants.LOCATE_FIND
posX = common.constants.LOCATE_COORDINATE_X
posY = common.constants.LOCATE_COORDINATE_Y
posFindButton = common.constants.LOCATE_FIND_BUTTON
posOK = common.constants.LOCATE_OK
center = common.constants.LOCATE_CENTER_SCREEN    
tuoc = common.constants.LOCATE_TUOC   
confirm = common.constants.LOCATE_CONFIRM   
close = common.constants.LOCATE_CLOSE   
import logging
from discord_client import DiscordClient
logging.basicConfig(level=logging.ERROR)
class GiveTitle(Task):
  
    def __init__(self, bot):
        super().__init__(bot)
    def do(self):
        print('give_title')
        super().back_to_map_gui()
        queues = [
            common.constants.TITLE_SCIENTIST,
            common.constants.TITLE_JUDGE,
            common.constants.TITLE_DUKE,
            common.constants.TITLE_ARCHITECT
        ]
     
        for title in queues:
            GiveTitle.checkGiveTitle(self,title)
            
        return True
    def checkGiveTitle(self,title):
        [pos,data] = GiveTitle.getResult(title)
        if len(pos) > 1 and len(data) > 0:
            first = data[0]
            x = first.x
            y = first.y
            timeRequest = first.timeRequest
            timeGiveTitle = first.timeGiveTitle
            time = first.time
          
            if timeGiveTitle == 0:
                result = self.startGive(x,y,pos)
                if result == True :
                    # self.discord.sendMess('Set title ' + Utils.getFullTitle(title) + ' success to : '+ str(x) +' ' +str(y))
                    first.timeGiveTitle = Utils.getCurrentTimeStamp()
                    Utils.updateData(title,0,first)
                else :
                    print('fail')
                    Utils.removeData(title,first)
            elif time*10 + timeGiveTitle < Utils.getCurrentTimeStamp():
                print('remove obj x = %s y = %s',x,y)
                Utils.removeData(title,first)
                self.checkGiveTitle(title)

    def getResult(title):
        pos = Utils.getPosByTitle(title)
        data = Utils.getData(title)
        return [pos,data]
    
    def startGive(self,x,y,posTuoc):
        print('give title x= %s y = %s ',x,y)
        # go to the town
        super().tap(posfind[0],posfind[1],1)
        super().tap(posX[0],posX[1],1)
        super().setText('' +x)
        super().tap(posOK[0],posOK[1],1)
        super().tap(posY[0],posY[1],1)
        super().setText(''+y)
        super().tap(posOK[0],posOK[1],1)
        super().tap(posFindButton[0],posFindButton[1],2)
        super().tap(center[0],center[1],1)
        # ban tuoc
        found, name, pos = self.gui.check_any(
                        ImagePathAndProps.TITLE_IMG_PATH.value,)
        if found :
            x,y = pos
            print('start x= %s y = %s ',posTuoc[0],posTuoc[1])
            super().tap(x,y,1)
            foundCheck, name, posCheck = self.gui.check_any(
                        ImagePathAndProps.CHECKED_BUTTON_IMAGE_PATH.value)
            if foundCheck:
                super().tap(close[0],close[1],1)
                return False
            else :
                super().tap(posTuoc[0],posTuoc[1],1)
                super().tap(confirm[0],confirm[1],1)
            return True
        else :
            super().tap(center[0],center[1],1)
        return False
        