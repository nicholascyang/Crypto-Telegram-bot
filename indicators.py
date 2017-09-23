#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import urllib2
import json
import time
import rigInfo

recipient = 9505687
token = '403145270:AAEArF39egMxyLsH-J8Lp0EYubjq8KwXFzU'

coins = [['OMG', 40, True], ['NEO', 40, True], ['MCO', 40, True],
         ['PAY', 40, True], ['UBQ', 40, True], ['XRP', 40, True],
         ['QWARK', 40, True]]
interval = 'DAY'
# values for stochastic indicator
K = 10
D = 5


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


def checkStochastic(interval, K, D):
    print 'starting stochastic check..'
    bot = telegram.Bot(token=token)
    coins = [['OMG', 40, True], ['NEO', 40, True], ['MCO', 40, True],
             ['PAY', 40, True], ['UBQ', 40, True], ['XRP', 40, True],
             ['QWARK', 40, True]]
    while True:
        for coin in coins:
            # get data from bittrex
            url = 'https://bittrex.com/Api/v2.0/pub/market/' + \
                  'GetTicks?marketName=BTC-%s&tickInterval=%s' % (coin[0],
                                                                  interval)
            urlOpen = urllib2.urlopen(url).read()
            tickData = json.loads(urlOpen)

            # initial high and lows
            low = 999999.0
            high = 0.0
            total = 0

            # find high and low
            for i in range(D):
                if tickData['success'] is True:
                    for value in tickData['result'][-K:]:
                        if value['L'] < low:
                            low = value['L']
                        if value['H'] > high:
                            high = value['H']
                else:
                    print 'could not get data'

                curClose = tickData['result'][-1]['C']
                stoch = (curClose - low)/(high - low) * 100
                del tickData['result'][-1:]
                total += stoch
            SmoothK = total/D
            coin[1] = SmoothK

            if SmoothK > 75:
                if coin[2] is True:

                    msg = '📈<b>%s</b> stochastic %s on <b>%s</b> \n' \
                           'interval currently at: <b>%s</b>' % \
                           (coin[0], 'rose above 75', interval, coin[1])
                    print msg
                    bot.send_message(chat_id=recipient,
                                     text=msg,
                                     parse_mode=telegram.ParseMode.HTML)
                    coin[2] = False
            elif SmoothK < 25:
                if coin[2] is True:
                    msg = '📉<b>%s</b> stochastic %s on <b>%s</b> \n' \
                          'interval currently at: <b>%s</b>' % \
                           (coin[0], 'fell below 25', interval, coin[1])
                    bot.send_message(chat_id=recipient,
                                     text=msg,
                                     parse_mode=telegram.ParseMode.HTML)
                    coin[2] = False
            elif coin[2] is False:
                    msg = '📉<b>%s</b> stochastic %s on <b>%s</b> \n' \
                          'interval currently at: <b>%s</b>' % \
                           (coin[0], 'back to neutral', interval, coin[1])
                    bot.send_message(chat_id=recipient,
                                     text=msg,
                                     parse_mode=telegram.ParseMode.HTML)
                    coin[2] = True
        time.sleep(360)


# def checkUbiq(bot, update):
#     wallet = '0x1e97007846d1F9368Bf7482C4F546fD1E6E1cF48'
#     prevBeat = 1405058895
#     tempPayout = 0
#     refreshrate = 1800

#     # check if a worker is offline
#     while True:
#         urlOpen = urllib2.urlopen('https://ubiqpool.io/api/accounts/' + wallet).read()
#         # read Json
#         ubiqJson = json.loads(urlOpen)
#         latestPayout = ubiqJson['payments'][0]['amount']

#         # new payout?
#         if latestPayout != tempPayout:
#             amount = Decimal(latestPayout) / 1000000000
#             payMsg = '💰New Ubiq payout for: ' + str(amount)
#             bot.send_message(chat_id=update.message.chat_id, text=payMsg)
#             print payMsg
#             tempPayout = latestPayout

#         # check if workers are offline
#         for worker in ubiqJson['workers']:
#             curWorker = worker
#             status = ubiqJson['workers'][worker]['offline']
#             lastBeat = ubiqJson['workers'][worker]['lastBeat']
#             if status is True and lastBeat > prevBeat:
#                 msg = "Worker " + curWorker + " is offline!"
#                 prevBeat = lastBeat
#                 bot.send_message(chat_id=update.message.chat_id,
#                                  text=msg)
#                 print msg


#         time.sleep(refreshrate)
