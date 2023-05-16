import telegram
import asyncio
from dotenv import dotenv_values

values = dotenv_values('env/tele.env')
BOT_API = values['BOT_API']
USER_ID = values['USER_ID']

class Bot:

    bot = telegram.Bot(BOT_API)
    loop = asyncio.new_event_loop()

    def __init__(self) -> None:
        print('Initializing bot...')
    
    def send(self, message:str):
        print(f'Sending Telegram message: {message}')
        self.loop.run_until_complete(self.bot.send_message(USER_ID, message))

def start_bot() -> Bot:
    bot = Bot()
    bot.send('Bot online.')
    return bot