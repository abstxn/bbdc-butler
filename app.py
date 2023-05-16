from tele import start_bot
from session import get_token
from query import checkExists
import message
import time

bot = start_bot()
token = get_token()

while True:
    reply = checkExists.send_using(token)
    if reply == message.EXPIRED_TOKEN:
        print('Token has expired. Waiting 5 minutes to perform re-authentication...')
        time.sleep(300)
        token = get_token()
    elif reply != message.NO_SLOT_RELEASED:
        print('Found slots.')
        bot.send('Slots detected!')
    time.sleep(15)