import time
import urllib.request, json
from urllib.request import Request
from web.models import Lectura, Address, PriceSnapshot,Cryptocurrency

def lanzar_lecturas():

    #https://ethereum.miningpoolhub.com/
    #https://auroracoin-qubit.miningpoolhub.com/index.php?page=api&action=getminingandprofitsstatistics&api_key=9aa20967691e0c3b4cdde30b8cd3d2e68815ae685681673fa6d9acd964ef8917


    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'
    BTC = Cryptocurrency.objects.get(pk=1)

    try:
        coindesk_url = urllib.request.urlopen(Request(str("https://api.coindesk.com/v1/bpi/currentprice/btc.json"), data=None, headers={'User-Agent': user_agent}))
        coindesk_data = json.loads(coindesk_url.read().decode())
        coindesk_USD = coindesk_data['bpi']['USD']['rate_float']
        PriceSnapshot().add_new(coindesk_USD,BTC)
    except:
        coindesk_USD = False

    for dire in Address.objects.all():
        btc_address = dire.address
        try:
            ahashpool_url = urllib.request.urlopen("https://www.ahashpool.com/api/wallet/?address="+btc_address)
            ahashpool_data = json.loads(ahashpool_url.read().decode())
            total_balance = ahashpool_data['total_earned']
            ahashpool_total = ahashpool_data['total_unpaid']
            Lectura().add_new(dire,1,ahashpool_total,dire.cryptocurrency,total_balance)
            # if coindesk_USD:

        except:
            ahashpool_total = 0

        try:
            zergpool_url = urllib.request.urlopen("http://www.zergpool.com//api/wallet/?address="+btc_address)
            zergpool_data = json.loads(zergpool_url.read().decode())
            total_balance = zergpool_data['total']
            zergpool_total = zergpool_data['unpaid']
            Lectura().add_new(dire,2,zergpool_total,dire.cryptocurrency,total_balance)
        except:
            zergpool_total = 0

        try:
            zpool_url = urllib.request.urlopen(Request(str("http://zpool.ca/api/wallet/?address="+btc_address), data=None, headers={'User-Agent': user_agent}))
            zpool_data = json.loads(zpool_url.read().decode())
            total_balance = zpool_data['total']
            zpool_total = zpool_data['unpaid']
            Lectura().add_new(dire,3,zpool_total,dire.cryptocurrency,total_balance)
        except:
            zpool_total = 0

        try:
            hashrefinery_url = urllib.request.urlopen(Request(str("http://pool.hashrefinery.com/api/wallet?address="+btc_address), data=None, headers={'User-Agent': user_agent}))
            hashrefinery_data = json.loads(hashrefinery_url.read().decode())
            total_balance = hashrefinery_data['total']
            hashrefinery_total = hashrefinery_data['unpaid']
            Lectura().add_new(dire,4,hashrefinery_total,dire.cryptocurrency,total_balance)
        except:
            hashrefinery_total = 0

        lecturas = []
        total = 0.0
        total_balance = 0.0
        for pool in Lectura().POOLS:
            if pool[0] > 0:
                lec = Lectura.objects.filter (address=dire,pool=pool[0]).order_by('-id')[0]
                lecturas.append(lec)
                total +=  lec.cash
                total_balance +=  lec.total_balance
        Lectura().add_new(dire,0,total,dire.cryptocurrency,total_balance)
