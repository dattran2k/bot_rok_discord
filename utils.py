from ast import Constant
import json
import time
import calendar

from numpy import tile
import data.data_list
from filepath.file_relative_paths import FilePaths
import common.constants
import logging
import pytesseract as tess
import sys
import os
import cv2
import inspect
import ctypes

import json
import traceback
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
        elif title == common.constants.TITLE_JUDGE :
            return 'Judge'
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
        elif title == common.constants.TITLE_JUDGE :
            return common.constants.JUDGE_DATA
        else :
            return ''

    def addToFile(path,x,y,title):
        time = Utils.getCurrentTimeStamp()
        object = {'x' : x,'y' : y,'title' : title,'timeRequest' : time,'time' : 1,'timeGivetitle' :0}
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
    def readDataFromFile(path):
        jsonFile = open(path, "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        return data
    def getPosByTitle(title):
        switcher = {
            common.constants.TITLE_ARCHITECT : common.constants.LOCATE_ARCHITECT,
            common.constants.TITLE_DUKE : common.constants.LOCATE_DUKE,
            common.constants.TITLE_JUDGE : common.constants.LOCATE_JUDGE,
            common.constants.TITLE_SCIENTIST : common.constants.LOCATE_SCIENTIST,
        }
        return switcher.get(title,[])
    def readDataFromTitle(title):
        switcher = {
            common.constants.TITLE_ARCHITECT : common.constants.ARCHITECT_DATA,
            common.constants.TITLE_DUKE : common.constants.DUKE_DATA,
            common.constants.TITLE_JUDGE : common.constants.JUDGE_DATA,
            common.constants.TITLE_SCIENTIST : common.constants.SCIENTIST_DATA,
        }
        return Utils.readDataFromFile(switcher.get(title,''))
    def converTitle(title):
        if title in common.constants.LIST_TITLE_ARCHITECT :
            return common.constants.TITLE_ARCHITECT
        elif title in common.constants.LIST_TITLE_DUKE :
            return common.constants.TITLE_DUKE
        elif  title in common.constants.LIST_TITLE_JUDGE :
            return common.constants.TITLE_JUDGE
        elif title in common.constants.LIST_TITLE_SCIENTIST :
            return common.constants.TITLE_SCIENTIST
        return '' 
    def addToData(title,object):
        if title == common.constants.TITLE_ARCHITECT :
            data.data_list.Data.addArchitect(object)
        elif title == common.constants.TITLE_DUKE :
              data.data_list.Data.addDuke(object)
        elif title == common.constants.TITLE_JUDGE :
              data.data_list.Data.addJudge(object)
        elif title == common.constants.TITLE_SCIENTIST :
                data.data_list.Data.addScient(object)
        return True       
    def removeData(title,object):
        if title == common.constants.TITLE_ARCHITECT :
            data.data_list.Data.removeArchitect(object)
        elif title == common.constants.TITLE_DUKE :
              data.data_list.Data.removeDuke(object)
        elif title == common.constants.TITLE_JUDGE :
              data.data_list.Data.removeJudge(object)
        elif title == common.constants.TITLE_SCIENTIST :
                data.data_list.Data.removeScient(object)
        return True   
    def updateData(title,index,object):
        if title == common.constants.TITLE_ARCHITECT :
            data.data_list.Data.updateArchitect(index,object)
        elif title == common.constants.TITLE_DUKE :
              data.data_list.Data.updateDuke(index,object)
        elif title == common.constants.TITLE_JUDGE :
              data.data_list.Data.updateJudge(index,object)
        elif title == common.constants.TITLE_SCIENTIST :
                data.data_list.Data.updateScient(index,object)
        return True         
    def getData(title):
        print('get data : '+ title)
        if title == common.constants.TITLE_ARCHITECT :
            return data.data_list.Data.getArchitect()
        elif title == common.constants.TITLE_DUKE :
            return data.data_list.Data.getDuke()
        elif title == common.constants.TITLE_JUDGE :
            return data.data_list.Data.getJudge()
        elif title == common.constants.TITLE_SCIENTIST :
            return data.data_list.Data.getScient()
    def getGamePackageStart() :
        type = os.getenv('TYPE')
        if type == common.constants.TYPE_QT:
            return common.constants.PACKAGE_QUOC_TE_START
        else :
            return common.constants.PACKAGE_GAMOTA
    def getGamePackage() :
        type = os.getenv('TYPE')
        if type == common.constants.TYPE_QT:
            return common.constants.PACKAGE_QUOC_TE
        else :
            common.constants.PACKAGE_GAMOTA
    
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def build_command(program_path, *args):
    return [program_path, *args]
def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def img_remove_background_and_enhance_word(cv_image, lower, upper):
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lower, upper)

def img_to_string(pil_image):
    # pil_image.save(resource_path("test.png"))
    tess.pytesseract.tesseract_cmd = resource_path(FilePaths.TESSERACT_EXE_PATH.value)
    result = tess.image_to_string(pil_image, lang='eng', config='--psm 6') \
        .replace('\t', '').replace('\n', '').replace('\f', '')
    return result

def bot_print(msg):
    print(msg)
