import config
import telebot
import requests
import json
from decimal import *

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['c', 'crex', 'крекс'])
def send_welcome(message):
        r = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")
        d = r.json()
        last = Decimal(d['Tickers'][0]['Last'])
        low = Decimal(d['Tickers'][0]['LowPrice'])
        high = Decimal(d['Tickers'][0]['HighPrice'])
        vol = Decimal(d['Tickers'][0]['BaseVolume'])
        orders = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnOrderBook?request=[PairName=BTC_SLD]")
        a = orders.json()
        buy = Decimal(a['BuyOrders'][0]['CoinPrice'])
        bcoin = Decimal(a['BuyOrders'][0]['CoinCount'])
        scoin = Decimal(a['SellOrders'][0]['CoinCount'])
        sell = Decimal(a['SellOrders'][0]['CoinPrice'])
        bot.reply_to(message, 'Crex24.com:'+'\nPair Name: Btc-Soldo'+'\nLast Price:  ' + '{0:.8f}'.format(last)+'  Btc'+'\nLow Price:  ' + '{0:.8f}'.format(low)+
'Btc'+'\nHigh Price: '+'{0:.8f}'.format(high)+" Btc"+'\nVolume: '+'{0:.8f}'.format(vol)+" Btc"+'\nBuy: '+'{0:.8f}'.format(buy)+
' Btc'+'\nBuy Count: '+'{0:.2f}'.format(bcoin)+' Sld'+'\nSell: '+'{0:.8f}'.format(sell)+' Btc'+'\nSell Count: '+'{0:.2f}'.format(scoin)+' Sld')


@bot.message_handler(commands=['a', 'alpha', 'альфа'])
def send_welcome(message):
        params = {'limit' : 1}
        r = requests.get('https://btc-alpha.com/api/charts/SLD_BTC/D/chart', params = params)
        d = r.json()
        low = Decimal(d[0]['low'])
        high = Decimal(d[0]['high'])
        vol = Decimal(d[0]['volume'])
        params = {'limit_sell': 1, 'limit_buy': 1,'group':1,}
        alfa = requests.get("https://btc-alpha.com/api/v1/orderbook/SLD_BTC/", params=params)
        alfa_res = alfa.json()
        asell = Decimal(alfa_res['sell'][0]['price'])
        a_sell_coin = Decimal(alfa_res['sell'][0]['amount'])
        abuy = Decimal(alfa_res['buy'][0]['price'])
        a_buy_coin = Decimal(alfa_res['buy'][0]['amount'])

        bot.reply_to(message,'Btc-Alpha.com:'+ '\nPair Name: Btc-Soldo'+'\nLow Price:  ' + '{0:.8f}'.format(low)+'  Btc'+'\nHigh Price: '+'{0:.8f}'.format(high)+" Btc"+'\nVolume: '+'{0:.8f}'.format(vol)+" Sld"+
                     '\nBuy: '+'{0:.8f}'.format(abuy)+' Btc'+'\nBuy Count: '+'{0:.2f}'.format(a_buy_coin)+' Sld'+'\nSell: '+'{0:.8f}'.format(asell)+' Btc'+'\nSell Count: '+'{0:.2f}'.format(a_sell_coin)+' Sld')

@bot.message_handler(commands=['n', 'net'])
def send_welcome(message):
        daemon = requests.get('http://127.0.0.1:33712/getinfo')
        
        request = daemon.json()
        diff = Decimal(request['difficulty'])
        block = Decimal(request['height'])
        rate = (diff/20)/1000
        bot.reply_to(message,'Height:   '+format(block)+ '\nHashrate:  ''{0:.2f}'.format(rate)+'  KH/s'+'\nNet Difficulty: '+ format(diff))



       
                     
bot.polling()
