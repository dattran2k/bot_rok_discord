import json
import time
import calendar
import data.model
import common.constants
import logging
logging.basicConfig(level=logging.INFO)
class Utils:
    def fromJson(path) : 
        f = open(path)
        data = json.load(f)
        arr = []
        for i in data :
            arr.append(i)
        return arr
    def getCurrentTimeStamp() :
        current_GMT = time.gmtime()
        # ts stores timestamp
        ts = calendar.timegm(current_GMT)
        return ts
    
    def getFullTitle(title):
        if title == common.constants.TITLE_DUKE :
            return 'Duke'
        elif title == common.constants.TITLE_ARCHITECT :
            return 'Architect'
        elif title == common.constants.TITLE_SCIENTIST :
            return 'Scientist'
        else :
            return ''
    
    def getTitleEnum(title) : 
        return common.constants.Title(title)      
    
    def getPathByTitle(title) :
        if title == common.constants.TITLE_DUKE :
            return common.constants.DUKE_DATA
        elif title == common.constants.TITLE_ARCHITECT :
            return common.constants.ARCHITECT_DATA
        elif title == common.constants.TITLE_SCIENTIST :
            return common.constants.SCIENTIST_DATA
        else :
            return ''

    def addToFile(path,x,y,title):
   
        time = Utils.getCurrentTimeStamp()
        object = {'x' : x,'y' : y,'title' : title,'timeRequest' : time,'time' : 1}
        jsonFile = open(path, "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
         ## Working with buffered content
        data.append(object)
        ## Save our changes to JSON file
        jsonFile = open(path, "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        return True
      
       

    