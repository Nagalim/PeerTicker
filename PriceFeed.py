import jsonrpc
import urllib
import urllib2

def btce_usd_query():
 try: # btce
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://btc-e.com/api/2/ppc_usd/ticker'),timeout=3).read())['ticker']
  price = ret['last']
  volume = ret['vol']
 except:
  print 'unable to update price for PPC on BTC-e (USD)'
  return 0,0
 return price,volume

def btce_btc_query():
 try: # bitfinex
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://api.bitfinex.com/v1//pubticker/btcusd'), timeout = 3).read())
  btcprice = float(ret['last_price'])
 except:
  try: # coinbase
   ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://coinbase.com/api/v1/prices/spot_rate?currency=USD'), timeout = 3).read())
   btcprice = float(ret['amount'])
  except:
   try: # bitstamp
    ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://www.bitstamp.net/api/ticker/'), timeout = 3).read())
    btcprice = float(ret['last'])
   except:
    print 'unable to update price for BTC'
    return 0,0
 try: # btce
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://btc-e.com/api/2/ppc_btc/ticker'),timeout=3).read())['ticker']
  price = ret['last']*btcprice
  volume = ret['vol']*btcprice
 except:
  print 'unable to update price for PPC on BTC-e (BTC)'
  return 0,0
 return price,volume

def btc38_cny_query():
 try: # yahoo
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'), timeout = 3).read())
  for res in ret['list']['resources']:
   if res['resource']['fields']['name'] == 'USD/CNY':
    cnyprice = float(res['resource']['fields']['price'])
 except:
  print("unable to update CNY price from yahoo")
  try: # coindesk
   ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://api.coindesk.com/v1/bpi/currentprice/CNY.json'), timeout = 3).read())
   cnyprice = float(ret['bpi']['CNY']['rate']) / float(ret['bpi']['USD']['rate'])
  except:
   print("unable to update price for CNY")
   return 0,0
 try: # btc38
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('http://api.btc38.com/v1/ticker.php?c=ppc',headers={'User-Agent': ''}),timeout=3).read())['ticker']
  price = ret['last']/cnyprice
  volume = ret['vol']/cnyprice
 except:
  print 'unable to update price for PPC on btc38'
  return 0,0
 return price,volume

def jubi_cny_query():
 try: # yahoo
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'), timeout = 3).read())
  for res in ret['list']['resources']:
   if res['resource']['fields']['name'] == 'USD/CNY':
    cnyprice = float(res['resource']['fields']['price'])
 except:
  print("unable to update CNY price from yahoo")
  try: # coindesk
   ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://api.coindesk.com/v1/bpi/currentprice/CNY.json'), timeout = 3).read())
   cnyprice = float(ret['bpi']['CNY']['rate']) / float(ret['bpi']['USD']['rate'])
  except:
   print("unable to update price for CNY")
   return 0,0
 try: # jubi
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('http://www.jubi.com/api/v1/ticker/?coin=ppc',headers={'User-Agent': ''}),timeout=3).read())
  price = float(ret['last'])/cnyprice
  volume = float(ret['vol'])/cnyprice
 except:
  print 'unable to update price for PPC on jubi'
  return 0,0
 return price,volume

def poloniex_btc_query():
 try: # bitfinex
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://api.bitfinex.com/v1//pubticker/btcusd'), timeout = 3).read())
  btcprice = float(ret['last_price'])
 except:
  try: # coinbase
   ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://coinbase.com/api/v1/prices/spot_rate?currency=USD'), timeout = 3).read())
   btcprice = float(ret['amount'])
  except:
   try: # bitstamp
    ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://www.bitstamp.net/api/ticker/'), timeout = 3).read())
    btcprice = float(ret['last'])
   except:
    print 'unable to update price for BTC'
    return 0,0
 try: # poloniex
  ret = jsonrpc.loads(urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=returnTicker'),timeout=3).read())['BTC_PPC']
  price = float(ret['last'])*btcprice
  volume = float(ret['baseVolume'])*btcprice
 except:
  print 'unable to update price for PPC on poloniex'
  return 0,0
 return price,volume

prices=[btce_usd_query(),btce_btc_query(),btc38_cny_query(),jubi_cny_query(),poloniex_btc_query()]
wsum=0
vsum=0
for i in range(0,len(prices)):
 wsum=wsum+prices[i][0]*prices[i][1]
 vsum=vsum+prices[i][1]

print('price:',wsum/vsum,'USD')
