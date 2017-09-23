from telegram.ext import Updater
from telegram.ext import CommandHandler
import telegram
import logging
import functions
import threading
import indicators
import time


recipient = 9505687
token = '403145270:AAEArF39egMxyLsH-J8Lp0EYubjq8KwXFzU'

updater = Updater(token='403145270:AAEArF39egMxyLsH-J8Lp0EYubjq8KwXFzU')

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

print 'starting bot..'
# handlers
start_handler = CommandHandler('start', functions.start)
status_handler = CommandHandler('status', functions.status)

# threaded check for offline miner
statusThread = threading.Thread(target=functions.checkConnectable)
statusThread.start()
indicatorThread = threading.Thread(target=indicators.checkStochastic, args=('DAY', 10, 5))
indicatorThread.start()
# dispatch all handlers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(status_handler)

# let's get polling
updater.start_polling()
