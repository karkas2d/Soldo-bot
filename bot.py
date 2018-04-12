#!/usr/bin/python3.5

# -*- coding: utf-8 -*-

import cherrypy

import config

import telebot

import requests

import json

import botan

from decimal import *

from time import sleep



WEBHOOK_HOST = 'IP_ADDRESS'

WEBHOOK_PORT = 80

WEBHOOK_LISTEN = '0.0.0.0' 



WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату

WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу



WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)

WEBHOOK_URL_PATH = "/%s/" % (config.token)



bot = telebot.TeleBot(config.token)


# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)





@bot.message_handler(commands=['start','help'])

def send_welcome(message):

        bot.send_message(message.chat.id,

        "I'm here to help you with your Soldo Here's what you can do :" +

        u"\n\U0001F55C/current - Shows you the most important about SLD right now"+

        u"\n\U0001F4B2/usd - Get the current SLD/USD exchange rate"+ #либо ставить цену в долларе только по крексу

        u"\n\U0001F4B0/btc - Get the current SLD/BTC exchange rate"+ #цена в бтц по крексу

        u"\n\U0001F4CA/supply - Displays info about the SLD supply at the moment"+

        ###"\n"u'\U0001F4CC'"/volume - Outputs the 24H volume of Soldo"+

        u"\n\U0001F517/cap - Shows SLD current market cap"+

        "\n\n"+

        "I also have some shortcuts to help you inform others about Soldo : "+

        u"\n\U00002753/about - Display everything you need to know to get started with SLD"+

        u"\n\U0001F512/nodes Gives you a list of Soldo nodes"+

        u"\n\U0001F310/worldwide - Print a link of every local Soldo group"+

        u"\n\U0000270A/vote - Discover polls and vote for SLD"+

        u"\n\n\U0001F680 Soldo is a novel coin based on the modified Cryptonote PoW algorithm called SoftCrypton and other miners do not work with Soldo. If you want to start mine Soldo use /guide"+

        "\n\n\n"+

        "Use /start, and I'll display this message again"+

        "\nIf you have any question or suggestion, you can [contact me](https://t.me//sergeevalexey)."+

        u"\n\U0001F60A Donations help to develop the project  /donate"+

        "\nGo ahead, test it now !",parse_mode='Markdown',disable_web_page_preview=True)

        botan.track(botan.botan_token, message.chat.id, message,'start')





@bot.message_handler(commands=['usd'])

def send_welcome(message):

        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")

        q = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=USD_BTC]")

        btc = q.json()

        sld = w.json()

        last_sld = Decimal(sld['Tickers'][0]['Last']) #получили цену Сольдо в Бтц

        last_btc= Decimal(btc['Tickers'][0]['Last'])  #получили цену Бтц в долларах

        sld_usd = last_sld*last_btc

        bot.send_message(message.chat.id,u'\U0001F4B2 SLD is worth: *'+'{0:.4f}'.format(sld_usd)+' USD*',parse_mode='Markdown')

        botan.track(botan.botan_token, message.chat.id, message, 'USD')



@bot.message_handler(commands=['btc'])

def send_welcome(message):

        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")

        sld = w.json()

        sld_btc = Decimal(sld['Tickers'][0]['Last']) #Получили цену в БТЦ

        bot.send_message(message.chat.id,u'\U0001F4B0 SLD is worth: *'+'{0:.8f}'.format(sld_btc)+' Btc*',parse_mode='Markdown')

        botan.track(botan.botan_token, message.chat.id, message,'BTC')



@bot.message_handler(commands=['supply'])

def send_welcome(message):        

        url = "http://localhost:33712/json_rpc"

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

        bot.send_message(message.chat.id,u'\U0001F4CA Market supply: *'+'{0:.2f}'.format(t_sup)+' M/10 M* ('+'{0:.2f}'.format(proc)+' %)',parse_mode='Markdown')

        botan.track(botan.botan_token, message.chat.id, message,'supply')



@bot.message_handler(commands=['cap'])

def send_welcome(message):

        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")

        q = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=USD_BTC]")

        btc = w.json()

        sld = q.json()

        last_sld = Decimal(sld['Tickers'][0]['Last']) #получили цену Сольдо

        last_btc= Decimal(btc['Tickers'][0]['Last'])  #получили цену Бтц

        sld_usd = last_sld*last_btc #Цена Сольдо в долларах

        url = "http://localhost:33712/json_rpc"

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

        bot.send_message(message.chat.id,u'\U0001F517  Market cap :  *'+'{0:.0f}'.format(cap)+' USD*',parse_mode='Markdown')

        botan.track(botan.botan_token, message.chat.id, message,'CAP')



@bot.message_handler(commands=['current'])

def send_welcome(message):

        w = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=BTC_SLD]")

        sld = w.json()

        q = requests.get("https://api.crex24.com/CryptoExchangeService/BotPublic/ReturnTicker?request=[NamePairs=USD_BTC]")

        btc = q.json()

        last_sld = Decimal(sld['Tickers'][0]['Last']) #получили цену Сольдо в Бтц

        last_btc= Decimal(btc['Tickers'][0]['Last'])  #получили цену  Бтц в долларах

        sld_usd = last_sld*last_btc

        url = "http://localhost:33712/json_rpc"

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

        daemon = requests.get('http://localhost:33712/getinfo')

        request = daemon.json()

        diff = Decimal(request['difficulty'])

        block = Decimal(request['height'])

        rate = (diff/20)/1000

        

        bot.send_message(message.chat.id,

                         u'\U0001F4B0 SLD is worth: '+

                         '\n  *'+'{0:.4f}'.format(sld_usd)+' USD*'+

                         '\n  *'+'{0:.8f}'.format(last_sld)+' Btc*'+

                         u'\n\n\U0001F4CA Market supply: \n  *'+'{0:.2f}'.format(t_sup)+' M/10 M* ('+'{0:.2f}'.format(proc)+' %)'+

                         u'\n\n\U0001F517 Market cap :  \n  *'+'{0:.0f}'.format(cap)+' USD*'+

                         u'\n\n\U0001F30D Network stats:'+

                         '\n  Height: ' +format(block)+

                         '\n  Hashrate:  '+'{0:.2f}'.format(rate)+'  KH/s'+

                         '\n  Net Difficulty: '+ format(diff),parse_mode='Markdown')

        botan.track(botan.botan_token, message.chat.id, message,'current')



@bot.message_handler(commands=['about'])

def send_welcome(message):

        bot.send_message(message.chat.id,

                         u'\U00002753 Here are a few useful ressources about Soldo :'+

                         u'\n\U0001F449 [Official website](http://soldo.in/)'+

                         u'\n\U0001F449 [Latest news](http://soldo.in/news/)'+

                         u'\n\U0001F449 [Gui wallet](https://github.com/monselice/soldo/releases/) or [Cli Wallet](https://github.com/monselice/sld/releases/)'+

                         u'\n\U0001F449 [Bitcoin Talk Topic](https://bitcointalk.org/index.php?topic=2332011)'+

                         #u'\n\U0001F449 [Join us at Ryver](https://zzl.ryver.com/application/signup/members/h07SVMfFAvFRGiZ)'+

                         u'\n\U0001F449 [Discord](https://discord.gg/Y8g6B4y)'+

                         u'\n\U0001F449 [Twitter](https://twitter.com/Soldo_SLD/)'+



                         '\n\n Soldo price, charts and detailed metrics on [Coinlib](https://coinlib.io/coin/SLD/Soldo)'+

                         '\n\nCurrent charts on [Crex24.com](https://crex24.com/ru/exchange/SLD-BTC/) or /crex'+

                         '\nCurrent charts on [Btc-Alpha.com](https://btc-alpha.com/exchange/SLD_BTC/) or /alpha'+

                         

                         

                         '\n\nChat with the community with /worldwide'+

                         '\nGet the Soldo project roadmaps with /roadmap'+

                         '\nFind ways to help Soldo with /vote',parse_mode='Markdown',disable_web_page_preview=True)

        botan.track(botan.botan_token, message.chat.id, message,'about')



@bot.message_handler(commands=['roadmap'])

def send_welcome(message):

        bot.send_message(message.chat.id, 'Soldo Ecosystem White Paper PDF [link on website](http://dl.soldo.in/Soldo-WP-Rus.pdf)',parse_mode='Markdown',disable_web_page_preview=True)

        botan.track(botan.botan_token, message.chat.id, message,'RoadMap')





@bot.message_handler(commands=['worldwide'])

def send_welcome(message):

        bot.send_message(message.chat.id,

                         'Soldo communities:'+

                         '\n [Russian](https://t.me/soldo_russia)'+

                         '\n [English](https://t.me/SLD_Soldo)',parse_mode='Markdown',disable_web_page_preview=True)

        botan.track(botan.botan_token, message.chat.id, message,'WW')



@bot.message_handler(commands=['vote'])

def send_welcome(message):

        bot.send_message(message.chat.id,

                         u'\U0000270ACurrently open votes to support Soldo :'+

                         '\n  [Vote to add SLD on altcoinexchange.com](https://feedback.altcoinexchange.com/suggestions/3104/soldo-sld) (pending...'u'\U0001F55C)'+

                         '\n  [Vote to add SLD on nextexchange](https://nextexchange.featureupvote.com/suggestions/3163/soldo-sld) (pending...'u'\U0001F55C)'+

                         '\n  [Vote to add SLD on lescovex.com](https://lescovex.featureupvote.com/suggestions/5524/soldo-sld) (pending...'u'\U0001F55C)'+

                         '\n  [Vote to add SLD on c-cex.com](https://c-cex.com/?id=vote&coin=sld) (pending...'u'\U0001F55C)'+

                         '\n  [Vote to add SLD on quantadex.zendesk.com](https://quantadex.zendesk.com/hc/en-us/community/posts/360002787811-Soldo-SLD-) (pending...'u'\U0001F55C)'

                         ,parse_mode='Markdown',disable_web_page_preview=True)

        botan.track(botan.botan_token, message.chat.id, message,'vote')

                         

                         

@bot.message_handler(commands=['donate'])

def send_welcome(message):

        bot.send_message(message.chat.id,

                         'My SLD address: Le4GmJkTHXWc981pbrqnEv7gZREj6nNmKF3k53b3rmqCP2HqvNGpT7w7hM8d5CZG6VhJHpJUwPWZkMmtNdFhAaaEFd59Z7B')

        botan.track(botan.botan_token, message.chat.id, message,'donate')





@bot.message_handler(commands=['nodes'])

def send_welcome(message):

        bot.send_message(message.chat.id,

                         u'\U0001F512 Nodes list for wallet syncing :'+

                         '\n1 - s2.soldo.in:33712'+

                         '\n2 - s3.soldo.in:33712'+

                         '\n3 - s4.soldo.in:33712'+

                         '\n\nYou can use this nodes to connect your wallets instead of running your own daemons.')      





@bot.message_handler(commands=['guide'])

def send_welcome(message):

        bot.send_message(message.chat.id,

                        'These commands are common to wallets on all systems.'+
                        '\n/Daemon, /Wallet, /Miner command line arguments and commands.'+
                        '\nWhat system you use'+

                        ' /windows or /linux ?')
        
@bot.message_handler(commands=['Daemon'])

def send_welcome(message):

        bot.send_message(message.chat.id,
                         u'\U0001F449Arguments:'+
                         '\n*--data-dir*  - Specify data directory'+
                         '\n*--rpc-bind-ip* (=127.0.0.1)'+
                         '\n*--rpc-bind-port* (=33712)'+
                         u'\n\U0001F449Commands:'+
                         '\n*start_mining %wallet_address% %threads%* - Start mining in several threads to a given wallet address'+
                         '\n*stop_mining* - Stop mining'+
                         '\n*show_hr* - Show current mining hashrate'+
                         '\n*hide_hr* - Stop showing current mining hashrate'+
                         '\n*exit* - Save cache and exit sldd',parse_mode='Markdown')
                         
                         
@bot.message_handler(commands=['Miner'])

def send_welcome(message):

        bot.send_message(message.chat.id,
                         u'\U0001F449Arguments:'+
                         '\n*--help* - produce this help message and exit'+
                         '\n*--address* - Valid cryptonote miner address'+
                         '\n*--daemon-address* - Daemon host:port. If you use this option you must not use --daemon-host and --daemon-port options'+
                         '\n*--threads* - Mining threads count. Must not be greater than you concurrency level. Default value is your hardware concurrency level'+
                         '\n*--scan-time* - Blockchain polling interval (seconds). How often miner will check blockchain for updates'+
                         '\n*--log-level* - Log level. Must be 0..5',parse_mode='Markdown')

@bot.message_handler(commands=['Wallet'])

def send_welcome(message):

        bot.send_message(message.chat.id,
                         u'\U0001F449Arguments:'+
                         '\n*--wallet* - Use wallet'+
                         '\n*--generate-new-wallet* - Generate new wallet and save it to <arg> or <address>.wallet by default'+
                         '\n*--password* - Wallet password'+
                         '\n*--daemon-address* - Use daemon instance at <host>:<port>'+
                         '\n*--rpc-bind-ip* - Specify ip to bind rpc server'+
                         '\n*--rpc-bind-port* - Starts wallet as rpc server for wallet operations, sets bind port for server'+
                         u'\n\U0001F449Commands:'+
                         '\n*help* - Print help on wallet commands'+
                         '\n*address* - Show current wallet public address'+
                         '\n*balance* - Show current wallet balance'+
                         '\n*start_mining* - Start mining in daemon'+
                         '\n*stop_mining* - Stop mining in daemon'+
                         '\n*transfer* - Transfer amount to address with mixin count (transfer %mixin count(1..100)% %address% %amount%)',parse_mode='Markdown')
                         



                         



@bot.message_handler(commands=['windows'])

def send_welcome(message):

        bot.send_message(message.chat.id,

                        'Use /about and download last release.'+

                        '\nGUI Wallet now is beta release but it works. Download, run, enjoy. \nIf you need CLI read next:'+

                        '\n1.Download ZIP-archive and unpack it to a folder (c:\SLD). \nThis archive contains several apps and batch files:'+

                        '\nsldd.exe - coins daemon'+

                        '\nsldw.exe - wallet app'+

                        '\nsldm.exe - CPU solo miner app'+

                        '\nnew-wallet.bat - batch file to generate new wallet'+

                        '\ndaemon.bat - batch file to start coins daemon'+

                        '\nwallet.bat - batch file to start wallet app with your wallet file and password'+

                        '\nminer.bat - batch file to run mining'+

                        '\n\n2. Generating a new wallet:'+

                         '\nEdit new-wallet.bat file, change the name and location of your wallet file as well as password. Save it.'+

                         "\nDon't start daemon, but run new-wallet.bat instead. You will get new wallet file with password supplied as result."+

                         '\nWARINING - backup *.wallet file ASAP to another pc, remote location of flash drive.'+

                         '\n\n3. Edit a miner batch file:'+

                         '\nOpen *.wallet.address file in notepad and copy your SLD address to clipboard'+

                         '\nEdit miner.bat file, paste just copied address instead of default.'+

                         '\nChange number of mining threads if you need. Save'+

                         '\n\n4. Prepare a wallet batch file:'+

                         '\nEdit wallet.bat, change the name and location of your wallet file as well as password. Save'+

                         '\n\n5. Start the daemon:'+

                         '\nRun daemon.bat.'+

                         '\nWait to full sync.'+

                         '\nIf daemon will not find any seed - check your windows firewall and home/office router NAT and firewall rules.'+

                         '\n\n6. Start mining:'+

                         '\nStart miner.bat.')



@bot.message_handler(commands=['linux'])

def send_welcome(message):

        bot.send_message(message.chat.id,
                         'Dependencies: GCC 4.7.3 or later, CMake 2.8.6 or later, and Boost 1.56 or later.'+
                         '\nTo build run these commands:'+
                         '\nsudo apt install git'+
                         '\nsudo apt install cmake'+
                         '\nsudo apt install build-essential'+
                         '\nsudo apt install libboost-dev libboost-all-dev'+

                         '\ncd ~'+
                         '\ngit clone https://github.com/monselice/sld.git sld'+
                         '\ncd sld'+
                         '\nmkdir build'+
                         '\ncd build'+
                         '\ncmake ..'+
                         '\ncd ..'+
                         '\nmake'+
                         '\n\nThe resulting executables can be found in sld/build/release/src')
                         



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

        botan.track(botan.botan_token, message.chat.id, message,'crex')





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

        botan.track(botan.botan_token, message.chat.id, message,'alpha')



                        

# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)

bot.remove_webhook()



# Ставим заново вебхук

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,

                certificate=open(WEBHOOK_SSL_CERT, 'r'))



# Указываем настройки сервера CherryPy

cherrypy.config.update({

    'server.socket_host': WEBHOOK_LISTEN,

    'server.socket_port': WEBHOOK_PORT,

    'server.ssl_module': 'builtin',

    'server.ssl_certificate': WEBHOOK_SSL_CERT,

    'server.ssl_private_key': WEBHOOK_SSL_PRIV,
    'server.socket_timeout' : 320,
    'server.response.timeout':3000	

})



cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})           

                     
