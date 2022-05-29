from data.data_list import Data
from discord_client import DiscordClient
from task.give_title import GiveTitle
from task.task import Task
import threading
from threading import Lock
from utils import stop_thread
import time
from task.Constants import TaskName
from common.device_gui_detector import GuiDetector
from filepath.file_relative_paths import ImagePathAndProps, VERIFICATION_CLOSE_REFRESH_OK, VERIFICATION_VERIFY_TITLE
import random
from utils import Utils
import logging
logging.basicConfig(level=logging.INFO)
class Bot():
    def __init__(self, device,discord):
        self.curr_thread = None
        self.device = device
        self.daemon_thread = None
        self.discord = discord
        self.gui = GuiDetector(device)
        self.task = Task(self)
        self.give_title = GiveTitle(self)
        self.round_count =0 

    def start(self, fn):
        if self.daemon_thread is not None and self.daemon_thread.is_alive():
            stop_thread(self.daemon_thread)
            print('daemon_thread: {}', self.daemon_thread.is_alive())

        if self.curr_thread is not None and self.curr_thread.is_alive():
            stop_thread(self.curr_thread)
            print('curr_thread: {}', self.curr_thread.is_alive())
        self.daemon(fn)

    def stop(self):
        if self.daemon_thread is not None and self.daemon_thread.is_alive():
            stop_thread(self.daemon_thread)
            print('daemon_thread: {}', self.daemon_thread.is_alive())

        if self.curr_thread is not None and self.curr_thread.is_alive():
            stop_thread(self.curr_thread)
            print('curr_thread: {}', self.curr_thread.is_alive())
    def daemon(self, fn):
        def run():
            main_thread = threading.Thread(target=fn)
            self.curr_thread = main_thread
            main_thread.start()

            while True:
                if self.daemon_thread is None or not main_thread.is_alive():
                    break
                time.sleep(60)
                found, _, pos = self.gui.check_any(ImagePathAndProps.VERIFICATION_VERIFY_TITLE_IMAGE_PATH.value)
                if found:
                    found, _, pos = self.gui.check_any(ImagePathAndProps.VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH.value)
                    if not found:
                        stop_thread(main_thread)
                        time.sleep(1)
                        main_thread = threading.Thread(target=fn)
                        self.curr_thread = main_thread
                        main_thread.start()

        daemon_thread = threading.Thread(target=run)
        daemon_thread.start()
        self.daemon_thread = daemon_thread
        
    def do_task(self, curr_task=TaskName.GIVE_TITLE):
        tasks = [
            [self.give_title, 'giveTitle'],
        ]
        while True:
            print('run do_task')
            for task in tasks:
                curr_task = task[0].do()
            self.round_count = self.round_count + 1
            time.sleep(5)
        return