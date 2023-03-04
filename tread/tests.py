# from django.test import TestCase
#
import ccxt
import datetime
import tread.config as conf

# # Create your tests here.
exchange = ccxt.kucoin({
    'apiKey': conf.KUCOIN_API_KEY,
    'secret': conf.KUCOIN_SECRET_KEY,
    'password': conf.KUCOIN_PASSWORD,
    'enableRateLimit': True,
})

symbol = 'ETH3L-USDT'
today = datetime.datetime.now()
delta = datetime.timedelta(days=2)
day1 = today - delta
balance = exchange.fetch_balance()
print(balance['ETH3L'])
print(exchange.fetch_my_trades(symbol=symbol,since=int(day1.timestamp() * 1000) ,limit=100))
{'info': 
    {'symbol': 'ETH3L-USDT',
     'tradeId': '390599150680065', 
     'orderId': '637b4cb04b96dd0001bab0e7',
     'counterOrderId': '637b4383586e090001af1d36',
     'side': 'buy',
     'liquidity': 'taker',
     'forceTaker': False,
     'price': '0.000861',
     'size': '3484.3205',
     'funds': '2.9999999505',
     'fee': '0.0029999999505', 'feeRate': '0.001', 'feeCurrency': 'USDT', 'stop': '', 'tradeType': 'TRADE', 'type': 'limit', 'createdAt': 1669024944000}, 'id': '390599150680065', 'order': '637b4cb04b96dd0001bab0e7', 'timestamp': 1669024944000, 'datetime': '2022-11-21T10:02:24.000Z', 'symbol': 'ETH3L/USDT', 'type': 'limit', 'takerOrMaker': 'taker', 'side': 'buy', 'price': 0.000861, 'amount': 3484.3205, 'cost': 2.9999999505, 'fee': {'cost': 0.0029999999505, 'currency': 'USDT', 'rate': 0.001}, 'fees': [{'currency': 'USDT', 'cost': 0.0029999999505, 'rate': 0.001}]}