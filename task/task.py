from importlib.resources import Package
from turtle import st
from adb import tap
import common.constants
from data.data_list import Data
import utils
import time
import traceback
import common.twocaptcha as twocaptcha
import filepath.constants
import logging
from discord_client import DiscordClient
logging.basicConfig(level=logging.INFO)
class Task:
    def __init__(self,bot):
        self.bot = bot
        self.device = bot.device
        self.gui = bot.gui
        self.discord = bot.discord
        self.data = Data()
    def isRoKRunning(self):
        cmd = 'dumpsys window windows | grep mCurrentFocus'
        str = self.device.shell(cmd)
        return str.find(utils.Utils.getGamePackageStart()) != -1
    
    def runOfRoK(self):
        cmd = 'am start -n ' + utils.Utils.getGamePackageStart()
        str = self.device.shell(cmd)

    def stopRok(self):
        cmd = 'am force-stop '+ utils.Utils.getGamePackage()
        str = self.device.shell(cmd)
        
    def setText(self,text):
        cmd = 'input text ' + text
        self.device.shell(cmd)
        
    def tap(self, x, y, sleep_time=0.1, long_press_duration=-1):
        cmd = None
        if long_press_duration > -1:
            cmd = 'input swipe {} {} {} {} {}'.format(x, y, x, y, long_press_duration)
            sleep_time = long_press_duration / 1000 + 0.2
        else:
            cmd = 'input tap {} {}'.format(x, y)

        str = self.device.shell(cmd)
        time.sleep(sleep_time)
    def pass_verification(self):
        pos_list = None
        try:
            # self.set_text(insert='pass verification')
            print('pass verification')
            box = (400, 190, 880, 720)
            ok = [780, 680]
            img = self.gui.get_curr_device_screen_img()
            img = img.crop(box)
            pos_list = twocaptcha.solve_verification(img)
            if pos_list is None:
                self.set_text(insert='fail to pass verification')
                print('fail to pass verification')
                return None

            for pos in pos_list:
                print('tap %s %s ',400 + pos[0],190 + pos[1])
                self.tap(400 + pos[0],190 + pos[1], 1)
            self.tap(780, 680, 5)

        except Exception as e:
            self.tap(100, 100)
            traceback.print_exc()

        return pos_list
     # Map
    def back_to_map_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name()
            gui_name, pos = ['UNKNOW', None] if result is None else result
            if gui_name == filepath.constants.MAP:
                break
            elif gui_name == filepath.constants.HOME:
                x_pos, y_pos = pos
                self.tap(x_pos, y_pos)
            elif gui_name == filepath.constants.WINDOW:
                self.back(1)
            else:
                self.back(1)
            loop_count = loop_count + 1
            time.sleep(0.5)
        return loop_count
    
    def get_curr_gui_name(self):
        if not self.isRoKRunning():
            # self.set_text(insert='game is not running, try to start game')
            self.runOfRoK()
            start = time.time()
            end = start
            time.sleep(10)
            self.tap(120,120)
            while end - start <= 300 and self.isRoKRunning():
                result = self.gui.get_curr_gui_name()
                if result is None:
                    time.sleep(5)
                    end = time.time()
                else:
                    break

        pos_list = None
        while True:
            result = self.gui.get_curr_gui_name()
            gui_name, pos = ['UNKNOW', None] if result is None else result
            if gui_name == filepath.constants.VERIFICATION_VERIFY:
                self.tap(pos[0], pos[1], 5)
                pos_list = self.pass_verification()
            else:
                return result    
       # Action
    def back(self, sleep_time=0.5):
        cmd = 'input keyevent 4'
        self.device.shell(cmd)
        time.sleep(sleep_time)