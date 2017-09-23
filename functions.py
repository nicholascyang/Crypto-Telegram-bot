import rigInfo
import indicators
import threading
import time
import telegram


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello!")


def status(bot, update):
    # rig host list
    hostList = ['192.168.1.141', '192.168.1.136']
    # port for host address
    port = 3333
    for host in hostList:
        rigStatus = rigInfo.reportStatus(host, port)
        if rigStatus is not None:
            bot.send_message(chat_id=9505687, text=rigStatus)
        else:
            msg = host + ' is offline'
            bot.send_message(chat_id=9505687, text=msg)


def checkConnectable():
    print 'starting connection check..'
    token = '403145270:AAEArF39egMxyLsH-J8Lp0EYubjq8KwXFzU'
    bot = telegram.Bot(token=token)
    offline = []
    while True:
        # rig host list
        hostList = ['192.168.1.141', '192.168.1.136']
        # port for host address
        port = 3333
        for host in hostList:
                rigStatus = rigInfo.reportStatus(host, port)
                if rigStatus is None and host not in offline:
                    msg = host + ' is offline'
                    bot.send_message(chat_id=9505687, text=msg)
                    offline.append(host)
                elif rigStatus is not None and host in offline:
                    offline.remove(host)
                    msg = host + ' came online'
                    bot.send_message(chat_id=9505687, text=msg)
        time.sleep(60)
