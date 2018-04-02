import config
import telebot
import requests
import json
from decimal import *
from time import sleep

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.send_message(message.chat.id,
        "I'm here to help you with your Soldo Here's what you can do :" +
        "\n"u'\U0001F55C'"/current - Shows you the most important about SLD right now"+
        "\n"u'\U0001F4B2'"/usd - Get the current SLD/USD exchange rate"+
        "\n"u'\U0001F4B0'"/btc - Get the current SLD/BTC exchange rate"+
        "\n"u'\U0001F4CA'"/supply - Displays info about the SLD supply at the moment"+
        ###"\n"u'\U0001F4CC'"/volume - Outputs the 24H volume of Soldo"+
        "\n"u'\U0001F517'"/cap - Shows SLD current market cap"+  
        "\n\n"+
        "I also have some shortcuts to help you inform others about Soldo : "+
        "\n"u'\U00002753'"/about - Display everything you need to know to get started with SLD"+
        "\n"u'\U0001F310'"/worldwide - Print a link of every local Soldo group"+
        "\n"u'\U0000270A'"/vote - Discover polls and vote for SLD"
        "\n\n\n"+
        "In case you need help, use /start, and I'll display this message again"+
        "\nIf you have any question or suggestion, you can [contact me](https://t.me//sergeevalexey)."+
        "\n\U0001F60A Donations help to develop the project  /donate"+
        "\nGo ahead, test it now !",parse_mode='Markdown',disable_web_page_preview=True)


@bot.message_handler(commands=['usd'])
def send_welcome(message):
        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")
        q = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=USD_BTC]")
        btc = q.json()
        sld = w.json()
        last_sld = Decimal(sld['Tickers'][0]['Last'])
        last_btc= Decimal(btc['Tickers'][0]['Last']) 
        sld_usd = last_sld*last_btc
        bot.send_message(message.chat.id,'\U0001F4B2 SLD is worth: *'+'{0:.4f}'.format(sld_usd)+' USD*',parse_mode='Markdown')

@bot.message_handler(commands=['btc'])
def send_welcome(message):
        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")
        sld = w.json()
        sld_btc = Decimal(sld['Tickers'][0]['Last']) 
        bot.send_message(message.chat.id,'\U0001F4B0 SLD is worth: *'+'{0:.8f}'.format(sld_btc)+' Btc*',parse_mode='Markdown')

@bot.message_handler(commands=['supply'])
def send_welcome(message):        
        url = "http://192.168.1.51:33712/json_rpc"
        headers = {'content-type': 'application/json'}
        rpc_input = {"method": "getlastblockheader"}
        rpc_input.update({"jsonrpc": "2.0", "id": "0"})
        get_hash = requests.post(url, data=json.dumps(rpc_input),headers=headers)
        result = json.dumps(get_hash.json()['result']['block_header']['hash'])
        hash = result.replace('"','')
        rpc_input = {"method": "block_json","params":{"hash" : hash}}
        get_block_info = requests.post(url,data=json.dumps(rpc_input),headers=headers)
        supply = json.dumps(get_block_info.json()['result']['block']['alreadyGeneratedCoins'])
        supply = int(supply.replace('"',''))
        t_sup = supply/100000000000000
        proc = supply/10000000000000
        bot.send_message(message.chat.id,'\U0001F4CA Market supply: *'+'{0:.2f}'.format(t_sup)+' M/10 M* ('+'{0:.2f}'.format(proc)+' %)',parse_mode='Markdown')

@bot.message_handler(commands=['cap'])
def send_welcome(message):
        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")
        q = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=USD_BTC]")
        btc = w.json()
        sld = q.json()
        last_sld = Decimal(sld['Tickers'][0]['Last']) 
        last_btc= Decimal(btc['Tickers'][0]['Last'])  
        sld_usd = last_sld*last_btc 
        url = "http://192.168.1.51:33712/json_rpc"
        headers = {'content-type': 'application/json'}
        rpc_input = {"method": "getlastblockheader"}
        rpc_input.update({"jsonrpc": "2.0", "id": "0"})
        get_hash = requests.post(url, data=json.dumps(rpc_input),headers=headers)
        result = json.dumps(get_hash.json()['result']['block_header']['hash'])
        hash = result.replace('"','')
        rpc_input = {"method": "block_json","params":{"hash" : hash}}
        get_block_info = requests.post(url,data=json.dumps(rpc_input),headers=headers)
        supply = json.dumps(get_block_info.json()['result']['block']['alreadyGeneratedCoins'])
        supply = int(supply.replace('"',''))
        t_sup = Decimal(supply/100000000)
        cap = sld_usd*t_sup
        bot.send_message(message.chat.id,'\U0001F517  Market cap :  *'+'{0:.0f}'.format(cap)+' USD*',parse_mode='Markdown')

@bot.message_handler(commands=['current'])
def send_welcome(message):
        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")
        sld = w.json()
        q = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=USD_BTC]")
        btc = q.json()
        last_sld = Decimal(sld['Tickers'][0]['Last'])
        last_btc= Decimal(btc['Tickers'][0]['Last'])  
        sld_usd = last_sld*last_btc
        url = "http://192.168.1.51:33712/json_rpc"
        headers = {'content-type': 'application/json'}
        rpc_input = {"method": "getlastblockheader"}
        rpc_input.update({"jsonrpc": "2.0", "id": "0"})
        get_hash = requests.post(url, data=json.dumps(rpc_input),headers=headers)
        result = json.dumps(get_hash.json()['result']['block_header']['hash'])
        hash = result.replace('"','')
        rpc_input = {"method": "block_json","params":{"hash" : hash}}
        get_block_info = requests.post(url,data=json.dumps(rpc_input),headers=headers)
        supply = json.dumps(get_block_info.json()['result']['block']['alreadyGeneratedCoins'])
        supply = int(supply.replace('"',''))
        t_sup = supply/100000000000000
        proc = supply/10000000000000
        t_sup_cap = Decimal(supply/100000000)
        cap = sld_usd*t_sup_cap
        daemon = requests.get('http://192.168.1.51:33712/getinfo')
        request = daemon.json()
        diff = Decimal(request['difficulty'])
        block = Decimal(request['height'])
        rate = (diff/20)/1000
        
        bot.send_message(message.chat.id,
                         '\U0001F4B0 SLD is worth: '+
                         '\n  *'+'{0:.4f}'.format(sld_usd)+' USD*'+
                         '\n  *'+'{0:.8f}'.format(last_sld)+' Btc*'+
                         '\n\n\U0001F4CA Market supply: \n  *'+'{0:.2f}'.format(t_sup)+' M/10 M* ('+'{0:.2f}'.format(proc)+' %)'+
                         '\n\n\U0001F517 Market cap :  \n  *'+'{0:.0f}'.format(cap)+' USD*'+
                         '\n\n\U0001F30D Network stats:'+
                         '\n  Height: ' +format(block)+
                         '\n  Hashrate:  '+'{0:.2f}'.format(rate)+'  KH/s'+
                         '\n  Net Difficulty: '+ format(diff),parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_welcome(message):
        bot.send_message(message.chat.id,
                         '\U00002753 Here are a few useful ressources about Soldo :'+
                         '\n\U0001F449 [Official website](http://soldo.in/)'+
                         '\n\U0001F449 [Latest news](http://soldo.in/news/)'+
                         '\n\U0001F449 [Gui wallet](https://github.com/monselice/soldo/releases/) or [Cli Wallet](https://github.com/monselice/sld/releases/)'+
                         '\n\nChat with the community with /worldwide'+
                         '\nGet the Soldo project roadmaps with /roadmap'+
                         '\nFind ways to help Bytecoin with /vote',parse_mode='Markdown',disable_web_page_preview=True)

@bot.message_handler(commands=['roadmap'])
def send_welcome(message):
        bot.send_message(message.chat.id, 'Soldo Ecosystem White Paper PDF [link on website](http://dl.soldo.in/Soldo-WP-Rus.pdf)',parse_mode='Markdown',disable_web_page_preview=True)


@bot.message_handler(commands=['worldwide'])
def send_welcome(message):
        bot.send_message(message.chat.id,
                         'Soldo communities:'+
                         '\n [Russian](https://t.me/soldo_russia)'+
                         '\n [English](https://t.me/SLD_Soldo)',parse_mode='Markdown',disable_web_page_preview=True)

@bot.message_handler(commands=['vote'])
def send_welcome(message):
        bot.send_message(message.chat.id,
                         '\U0000270ACurrently open votes to support Soldo :'+
                         '\n  [Vote to add SLD on altcoinexchange.com](https://feedback.altcoinexchange.com/suggestions/3104/soldo-sld) (pending...\U0001F55C)'+
                         '\n  [Vote to add SLD on nextexchange](https://nextexchange.featureupvote.com/suggestions/3163/soldo-sld) (pending...\U0001F55C)'+
                         '\n  [Vote to add SLD on lescovex.com](https://lescovex.featureupvote.com/suggestions/5524/soldo-sld) (pending...\U0001F55C)'+
                         '\n  [Vote to add SLD on c-cex.com](https://c-cex.com/?id=vote&coin=sld) (pending...\U0001F55C)'+
                         '\n  [Vote to add SLD on quantadex.zendesk.com](https://quantadex.zendesk.com/hc/en-us/community/posts/360002787811-Soldo-SLD-) (pending...\U0001F55C)'
                         ,parse_mode='Markdown',disable_web_page_preview=True)
                         
                         
@bot.message_handler(commands=['donate'])
def send_welcome(message):
        bot.send_message(message.chat.id,
                         'My SLD address: Le4GmJkTHXWc981pbrqnEv7gZREj6nNmKF3k53b3rmqCP2HqvNGpT7w7hM8d5CZG6VhJHpJUwPWZkMmtNdFhAaaEFd59Z7B')


                        
 
@bot.message_handler(commands=['c', 'crex'])
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


@bot.message_handler(commands=['a', 'alpha'])
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

                        
                         
                         
                         

while True:

    try:

        bot.polling(none_stop=True)

    except Exception as e:

        logger.error(e)

        time.sleep(15)
