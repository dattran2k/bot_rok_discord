import adb
import sys
from discord_client import DiscordClient
from task.bot import Bot
import discord
from gui.main_window import MainWindow
from data.data_list import Data
import threading
sys.path.append('/.../')

def main():
    adb.bridge = adb.enable_adb()
    device = adb.bridge.get_device('127.0.0.1',21523)
    discordClient = DiscordClient()
    mythread = threading.Thread(target=discordClient.startRun)
    mythread.start()
    bot = Bot(device,discordClient)
    Bot.start(bot,bot.do_task)
    # device.shell("logcat", handler=dump_logcat)
    window = MainWindow()
    window.run()


def dump_logcat(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print(data.decode('utf-8'))
    connection.close()
if __name__ == '__main__':
    main()
