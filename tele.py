'''
Module encapsulates an instance of a Telegram bot's chat with a particular user.
'''

import telegram
import asyncio

class Bot:

    api_token = None
    tele_user_ID = None
    bot_instance = None

    cache_file_dir = './secrets/telegram-info'
    loop = asyncio.new_event_loop()

    def __init__(self):
        file = open(self.cache_file_dir, 'r')
        lines = file.readlines()
        self.api_token = lines[0].rstrip()
        self.tele_user_ID = lines[1].rstrip()
        self.bot_instance = telegram.Bot(self.api_token)
    
    def send(self, message:str):
        self.loop.run_until_complete(self.bot_instance.send_message(self.tele_user_ID, message))
    
    def stop(self):
        self.loop.close()


def start() -> Bot:
    return Bot()