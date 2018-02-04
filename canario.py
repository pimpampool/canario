#!/usr/bin/python
import time
import urllib.request, json
from urllib.request import Request
import os


btc_address = "1KsPftfHwNsawVS3uVRDFs5sL9Tb1XzZxo"
#btc_address = "18vci4opZHXnYUBsSz9qYGhWXA6WjfAD2S"
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'





def showme_the_money():
    try:
        ahashpool_url = urllib.request.urlopen("https://www.ahashpool.com/api/wallet/?address="+btc_address)
        ahashpool_data = json.loads(ahashpool_url.read().decode())
        ahashpool_total = ahashpool_data['total_earned']
    except:
        ahashpool_total = 0

    try:
        zergpool_url = urllib.request.urlopen("http://www.zergpool.com//api/wallet/?address="+btc_address)
        zergpool_data = json.loads(zergpool_url.read().decode())
        zergpool_total = zergpool_data['total']
    except:
        zergpool_total = 0

    try:
        zpool_url = urllib.request.urlopen(Request(str("http://zpool.ca/api/wallet/?address="+btc_address), data=None, headers={'User-Agent': user_agent}))
        zpool_data = json.loads(zpool_url.read().decode())
        zpool_total = zpool_data['total']
    except:
        zpool_total = 0

    try:
        hashrefinery_url = urllib.request.urlopen(Request(str("http://pool.hashrefinery.com/api/wallet?address="+btc_address), data=None, headers={'User-Agent': user_agent}))
        hashrefinery_data = json.loads(hashrefinery_url.read().decode())
        hashrefinery_total = hashrefinery_data['total']
    except:
        hashrefinery_total = 0

    coindesk_url = urllib.request.urlopen(Request(str("https://api.coindesk.com/v1/bpi/currentprice/btc.json"), data=None, headers={'User-Agent': user_agent}))
    coindesk_data = json.loads(coindesk_url.read().decode())
    coindesk_USD = coindesk_data['bpi']['USD']['rate_float']
    pool_totals = ahashpool_total+zergpool_total+zpool_total+hashrefinery_total



    os.system('cls')
    os.system('clear')

    def btc_to_usd(btc):
        usd = 1.0*btc*coindesk_USD
        return str(float("{0:.2f}".format(usd)))+ ' $'


    print('BTC -> '+str(int(coindesk_USD))+' $')
    print('----------------')
    print('ahashpool')
    print(str(ahashpool_total)+'    '+ btc_to_usd(ahashpool_total) )
    print('----------------')
    print('zergpool')
    print(str(zergpool_total)+'    '+  btc_to_usd(zergpool_total) )
    print('----------------')
    print('zpool')
    print(str(zpool_total)+'    '+  btc_to_usd(zpool_total) )
    print('----------------')
    print('hashrefinery')
    print(str(hashrefinery_total)+'    '+  btc_to_usd(hashrefinery_total) )
    print('----------------')
    print()
    print('##### TOTAL ####')
    print(str(pool_totals) +'    '+  btc_to_usd(pool_totals))



while True:
    showme_the_money()
    time.sleep(20)
    print('Actualizando')
