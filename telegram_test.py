import time
import asyncio
import telegram

class Telegram_Details:

    bot_token = 'NOT_INITIALIZED'
    telegram_UID = 'NOT_INITIALIZED' # see @userinfobot in Telegram

    def __init__(self, bot_token: str, telegram_UID: str):
        self.bot_token = bot_token
        self.telegram_UID = telegram_UID 
    
    @classmethod
    def read_cache(cls):
        try:
            cached_file = open('.telegram', 'r')
            text_lines = cached_file.readlines()
            bot_token = text_lines[0].rstrip()
            telegram_UID = text_lines[1].rstrip()
            return cls(bot_token, telegram_UID)
        except FileNotFoundError:
            print('File containing Telegram details (bot token, user ID) not found. Aborting.')
            exit(1)

class Telegram_Connection:

    telegram_UID: str = None
    bot_instance: telegram.Bot = None

    def __init__(self, telegram_details: Telegram_Details):
        self.telegram_UID = telegram_details.telegram_UID
        self.bot_instance = telegram.Bot(telegram_details.bot_token)
        print('Initialized Telegram bot.')
    
    async def send(self, message: str):
        await self.bot_instance.send_message(self.telegram_UID, message)
    
    async def notify_available_slot(self, slot):
        notification = f'Available slot:\n\n{slot}'
        await self.bot_instance.send_message(self.telegram_UID, notification)

telegram_details = Telegram_Details.read_cache()
telegram_connection = Telegram_Connection(telegram_details)

main_loop = asyncio.new_event_loop()
main_loop.run_until_complete(telegram_connection.send("Bot online."))

async def query_slots():
    i = 0
    while True:
        if i > 10:
            await telegram_connection.send("Available slots detected! GO GO GO!")
            break
        else:
            print(i)
            i += 1
            await asyncio.sleep(1)

main_loop.run_until_complete(query_slots())
main_loop.close()