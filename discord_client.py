from dis import dis
from http import client
import os
import queue
import discord
import logging
logging.basicConfig(level=logging.INFO)
from numpy import tile
import pandas as pd
import sys
from data.data_list import Data
sys.path.append('/.../common/')
sys.path.append('/.../')
from utils import Utils
import asyncio
# import do 

import common.constants

from dotenv import load_dotenv
load_dotenv()


KEY = os.getenv('key')
class DiscordClient(discord.Client):
    
    def startRun(self):
        self.run(KEY)
        
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        await self.change_presence(activity=discord.Game('Client is runing Type _hint to get example'))
        # self.sendMess("Bot started, let's gooooooooooooooooooooooooooo !!!!")

    def sendMess(self,message):
        answer = discord.Embed(title="Message from server :",
                                        description=message,
                                        colour=0x1a7794) 
        c = self.get_channel(os.getenv('CHANNEL_ID'))
        asyncio.gather(c.send(embed = answer))

    async def on_message(self,message):
        client = self
        if message.author == client.user:
            return
        if message.content.startswith(common.constants.CMD_GIVE_TITLE) :
            data = message.content.replace(common.constants.CMD_GIVE_TITLE,"").split()
            if len(data) == 3 :
                x = data[0]
                y = data[1]
                title = Utils.converTitle(data[2])
                # do.ban_tuoc(x,y,tuoc)
                answer = None
                # path = Utils.getPathByTitle(title)
                #  result = Utils.addToFile(path,x,y,title)
                queue = Utils.getData(title)
                time = Utils.getCurrentTimeStamp()
                object = Data(x=x,y=y,title=title,timeRequest=time,timeGiveTitle=0,time = 1)
                result = Utils.addToData(title,object)
                if result:                  
                    if queue == None:
                        answer = discord.Embed(title="ERROR ",
                                        description="Some thing wrong",
                                        colour=0xde3f1f) 
                    elif len(queue) == 0:
                        answer = discord.Embed(title="Nice you are the first one : " + Utils.getFullTitle(title),
                                        description="comming soon",
                                        colour=0x1a7794)  
                    else :
                        answer = discord.Embed(title="Add to queue: " + Utils.getFullTitle(title),
                                        description="Please Wait. queue = "+ str(len(queue)),
                                        colour=0x1a7794) 
                else:
                    answer = discord.Embed(title="ERROR ",
                                        description="Some thing wrong",
                                        colour=0xde3f1f) 
                await message.channel.send(embed=answer)
        elif message.content.startswith(common.constants.CMD_HINT) :
            answer = discord.Embed(title="Hint is here : " ,
                                        description= common.constants.HINT,
                                        colour=0x1a7794) 
            await message.channel.send(embed=answer)
        return
        if message.content.startswith('_'):
            cmd = message.content.split()[0].replace("_","")
            if len(message.content.split()) > 1:
                parameters = message.content.split()[1:]

            # Bot Commands

            if cmd == 'scan':
                data = pd.DataFrame(columns=['content', 'time', 'author'])

                # Acquiring the channel via the bot command
                if len(message.channel_mentions) > 0:
                    channel = message.channel_mentions[0]
                else:
                    channel = message.channel

                # Aquiring the number of messages to be scraped via the bot command
                if (len(message.content.split()) > 1 and len(message.channel_mentions) == 0) or len(message.content.split()) > 2:
                    for parameter in parameters:
                        if parameter == "help":
                            answer = discord.Embed(title="Command Format",
                                                description="""`_scan <channel> <number_of_messages>`\n\n`<channel>` : **the channel you wish to scan**\n`<number_of_messages>` : **the number of messages you wish to scan**\n\n*The order of the parameters does not matter.*""",
                                                colour=0x1a7794) 
                            await message.channel.send(embed=answer)
                            return
                        elif parameter[0] != "<": # Channels are enveloped by "<>" as strings
                            limit = int(parameter)
                else:
                    limit = 100
                
                answer = discord.Embed(title="Creating your Message History Dataframe",
                                    description="Please Wait. The data will be sent to you privately once it's finished.",
                                    colour=0x1a7794) 

                await message.channel.send(embed=answer)

                def is_command (message):
                    if len(msg.content) == 0:
                        return False
                    elif msg.content.split()[0] == '_scan':
                        return True
                    else:
                        return False

                async for msg in channel.history(limit=limit + 1000):       # The added 1000 is so in case it skips messages for being
                    if msg.author != client.user:                           # a command or a message it sent, it will still read the
                        if not is_command(msg):                             # the total amount originally specified by the user.
                            data = data.append({'content': msg.content,
                                                'time': msg.created_at,
                                                'author': msg.author.name}, ignore_index=True)
                        if len(data) == limit:
                            break
                
                # Turning the pandas dataframe into a .csv file and sending it to the user

                file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv" # Determining file name and location
                data.to_csv(file_location) # Saving the file as a .csv via pandas

                answer = discord.Embed(title="CSV của bố đây",
                                    description=f"""It might have taken a while, but here is what you asked for.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{limit}**""",
                                    colour=0x1a7794) 

                await message.author.send(embed=answer)
                await message.author.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
                os.remove(file_location) # Deleting the file
    
 