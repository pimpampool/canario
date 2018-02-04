from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import time
import urllib.request, json
from urllib.request import Request
from web.models import *
import json
from urllib.request import Request

def btc_to_usd(btc):
    usd = 1.0*btc*coindesk_USD
    return str(float("{0:.2f}".format(usd)))+ ' $'

def index(request):
    if request.method == 'POST':
        # nuevo = request.POST.get("nuevo", "")
        # if nuevo:
        addr = request.POST.get("address", "")
        return HttpResponseRedirect('./monitor/'+addr+'/0')
    template = loader.get_template('web/index.html')
    context = {
        'latest_question_list': 2,
    }
    return HttpResponse(template.render(context, request))



def monitor_pool(request,address,pool_id):
    # último precio del btc en USD
    btc_USD = PriceSnapshot.objects.all().order_by('-id')[0].price
    # balance del address en blockchain
    try:
        url = 'https://blockchain.info/q/addressbalance/'+address+'?confirmations=1'
        addr_balance =  int(urllib.request.urlopen(Request(url), data=None).read().decode())/100000000
    except:
        addr_balance = 'ERROR'

    addr = Address.objects.get(address=address)
    lecturas = []
    total = 0.0
    for pool in Lectura().POOLS:
        if pool[0] > 0:
            lec = Lectura.objects.filter (address=addr,pool=pool[0]).order_by('-id')[0]
            lec.usd = "{:.2f}".format(lec.cash * btc_USD)
            lecturas.append(lec)
            total +=  lec.cash
    total_usd = "{:.2f}".format(total * btc_USD)

    # Calcular beneficio 24 h
    from datetime import datetime, timedelta

    time_threshold = datetime.now() - timedelta(hours=24)
    last_24h_now = Lectura.objects.filter(address=addr,pool=0).order_by('-id')[0].cash
    try:
        last_24h_low = Lectura.objects.filter(address=addr,pool=0).filter(date__lt=time_threshold).order_by('-id')[0].cash
    except:
        last_24h_low = Lectura.objects.filter(address=addr,pool=0).order_by('id')[0].cash

    template = loader.get_template('web/monitor.html')
    context = {
        'address': addr,
        'pool': pool_id,
        'pool_name' : Lectura().POOLS[pool_id][1],
        'lecturas': lecturas,
        'btc_USD':"{:.2f}".format(btc_USD),
        'last_24h_btc' : "{:.8f}".format(last_24h_now - last_24h_low),
        'total_usd':total_usd,
        'addr_balance': addr_balance,
        'total': "{:.8f}".format(total) ,
    }
    return HttpResponse(template.render(context, request))


# @login_required
def chart_data_json(request,addr,pool_id):
    data = []
    params = request.GET
    addr = Address.objects.get(address=addr)
    lecturas = Lectura.objects.filter(address=addr,pool=pool_id)
    for lec in lecturas:
        data.append([int(lec.date.timestamp())*1000, lec.cash])

    return HttpResponse(json.dumps(data), content_type='application/json')
