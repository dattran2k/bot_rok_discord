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
import logging
logging.basicConfig(level=logging.ERROR)
class CheckVerifi(Task):
    def __init__(self, bot):
        super().__init__(bot)
    # def checkVerifi(self,Task):
    #     found, _, pos = self.gui.check_any(ImagePathAndProps.VERIFICATION_VERIFY_TITLE_IMAGE_PATH.value)
    #         if found:
    #             found, _, pos = self.gui.check_any(ImagePathAndProps.VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH.value)
    #             if n