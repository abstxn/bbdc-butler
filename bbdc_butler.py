'''
Main logic of bbdc-butler, and the entry point to the application.
'''

import tele
import session_token
from query import practical_exists
import message
import time

bot = tele.start()
bot.send("Bot is online!")

token = session_token.get()

while True:
    reply = practical_exists.query(token)
    if reply == message.EXPIRED_TOKEN:
        time.sleep(300)
        token = session_token.get()
    elif reply != message.NO_SLOT_RELEASED:
        bot.send('Slots detected!')
    time.sleep(5)

bot.stop()