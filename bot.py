import config
import telebot
import requests
import json
from decimal import *

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['c', 'crex'])
def send_welcome(message):
        r = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")
        d = r.json()
        last = Decimal(d['Tickers'][0]['Last'])
        low = Decimal(d['Tickers'][0]['LowPrice'])
        high = Decimal(d['Tickers'][0]['HighPrice'])
        vol = Decimal(d['Tickers'][0]['BaseVolume'])
        bot.reply_to(message, 'Crex24.com:'+'\nPair Name: Btc-Soldo'+'\nLast Price:  ' + '{0:.8f}'.format(last)+'  Btc'+'\nLow Price:  ' + '{0:.8f}'.format(low)+'  Btc'+'\nHigh Price: '+'{0:.8f}'.format(high)+" Btc"+'\nVolume: '+'{0:.8f}'.format(vol)+" Btc")


@bot.message_handler(commands=['a', 'alpha'])
def send_welcome(message):
        params = {'limit' : 1}
        r = requests.get('https://btc-alpha.com/api/charts/SLD_BTC/D/chart', params = params)
        d = r.json()
        low = Decimal(d[0]['low'])
        high = Decimal(d[0]['high'])
        vol = Decimal(d[0]['volume'])
        bot.reply_to(message,'Btc-Alpha.com:'+ '\nPair Name: Btc-Soldo'+'\nLow Price:  ' + '{0:.8f}'.format(low)+'  Btc'+'\nHigh Price: '+'{0:.8f}'.format(high)+" Btc"+'\nVolume: '+'{0:.8f}'.format(vol)+" Sld")

@bot.message_handler(commands=['n', 'net'])
def send_welcome(message):
        daemon = requests.get('http://127.0.0.1:33712/getinfo')
        request = daemon.json()
        diff = Decimal(request['difficulty'])
        block = Decimal(request['height'])
        rate = (diff/20)/1000
        bot.reply_to(message,'Height:   '+format(block)+ '\nHashrate:  ''{0:.2f}'.format(rate)+'  KH/s'+'\nNet Difficulty: '+ format(diff))



       
                     
bot.polling()
