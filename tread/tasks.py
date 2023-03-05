from celery import shared_task
# We can have either registered task
import pandas as pd
import requests
import ccxt
import datetime
import ta
import tread.config as conf
from ta.trend import MACD
from tread.algorithem.heikin_ashi import HA
import time
from django.utils import timezone
from .models import Coin, ExitAndEnterFactor
from transaction.models import Transaction

exchange = ccxt.kucoin({
    'apiKey': conf.KUCOIN_API_KEY,
    'secret': conf.KUCOIN_SECRET_KEY,
    'password': conf.KUCOIN_PASSWORD,
    'enableRateLimit': True,

})


@shared_task
def send_notifiction():
    query = Coin.objects.all()
    for data in query:
        print(data.symbol)
        sar_and_kijensen = indicator_calculation(data.symbol)
        time.sleep(1)
        transaction = get_last_tread(data.symbol)
        balance = exchange.fetch_balance()
        print(balance['total']['USDT'], balance['total'][data.name])
        if (int(balance['total']['USDT']) >= 1):
            if (condition_purchase(sar_kijensen=sar_and_kijensen)):
                print("purchase: True")
                order_all_buy(data.symbol)
                time.sleep(1)
        if (int(balance['total'][data.name])):
            if (transaction['status']):
                if (condition_sale(symbol=data.symbol, last_tread=transaction['data'], sar=sar_and_kijensen)):
                    order_all_sell(data.symbol, data.name)
                    time.sleep(1)
        time.sleep(1)


def order_all_buy(symbol):
    balance = exchange.fetch_balance()
    try:
        if (int(balance['total']['USDT']) >= 0):
            ask = get_bid_ask(symbol)[1]
            price = ask
            amount = int(balance['total']['USDT']) / ask
            trans = exchange.create_limit_buy_order(symbol=symbol, price=price, amount=amount)
            print("purchase buy: True")
            print(trans)
            buy = Transaction(symbol=trans['symbol'],
                              order_id=trans['info']['orderId'],
                              price=trans['price'],
                              amount=trans['amount'],
                              time_stamp=trans['timestamp'],
                              type='buy',
                              created_at=timezone.now())
            buy.save()
            return {'status': 'save buy transaction'}
        else:
            return {'status': 'No cash'}
    except:
        if (int(balance['total']['USDT']) >= 0):
            ask = get_bid_ask(symbol)[1]
            price = ask
            amount = int(balance['total']['USDT']) / ask
            trans = exchange.create_limit_buy_order(symbol=symbol, price=price, amount=amount)
            print("purchase buy: True")
            print(trans)
            buy = Transaction(symbol=trans['symbol'],
                              order_id=trans['info']['orderId'],
                              price=trans['price'],
                              amount=trans['amount'],
                              time_stamp=trans['timestamp'],
                              type='buy',
                              created_at=timezone.now())
            buy.save()
            return {'status': 'save buy transaction'}
        else:
            return {'status': 'No cash'}


def order_all_sell(symbol, name):
    bid = get_bid_ask(symbol)[0]
    balance = exchange.fetch_balance()
    try:
        if (balance['total'][name] >= 0):
            trans = exchange.create_limit_sell_order(symbol=symbol, price=bid, amount=balance['total'][name])
            buy = Transaction(symbol=trans['symbol'],
                              order_id=trans['info']['orderId'],
                              price=trans['price'],
                              amount=trans['amount'],
                              time_stamp=trans['timestamp'],
                              type='sell',
                              created_at=timezone.now())
            buy.save()
            return {'status': 'save'}
        else:
            return {'status': 'No cash'}
    except:
        return {'status': 'Err form exchange'}


def get_bid_ask(symbol):
    orderbook = exchange.fetch_order_book(symbol)
    bid = orderbook['bids'][0][0]
    ask = orderbook['asks'][0][0]
    return bid, ask


def indicator_calculation(symbol):
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=10)
    day2 = today - delta
    ohl_sar = None
    try:
        ohlc_sar = exchange.fetch_ohlcv(symbol, timeframe='5m', since=int(day2.timestamp() * 1000))
    except:
        time.sleep(1)
        ohlc_sar = exchange.fetch_ohlcv(symbol, timeframe='5m', since=int(day2.timestamp() * 1000))

    list_name = ['Date', 'Open', 'High', 'Low', 'Close', 'valume']
    df_sar = pd.DataFrame(ohlc_sar, columns=list_name)
    df_sar = HA(df_sar)
    out_sar = ta.trend.PSARIndicator(high=df_sar['HA_high'], close=df_sar['HA_close'], low=df_sar['HA_low'])
    df_sar['PSAR'] = out_sar.psar()
    out_ichimoku = ta.trend.IchimokuIndicator(high=df_sar['HA_high'], low=df_sar['HA_low'])
    out_macd = ta.trend.MACD(close=df_sar['HA_close'])
    df_sar['Macd'] = out_macd.macd()
    df_sar['Macd_signal'] = out_macd.macd_signal()
    df_sar['Kijensen'] = out_ichimoku.ichimoku_base_line()  # ichimoku_base_line == kijensen
    return df_sar.iloc[-1]['HA_close'], df_sar.iloc[-1]['PSAR'], df_sar.iloc[-1]['Kijensen'], df_sar.iloc[-1]['Macd'], \
    df_sar.iloc[-1]['Macd_signal']


def condition_purchase(sar_kijensen):
    if (
            sar_kijensen[0] > sar_kijensen[1] and sar_kijensen[0] > sar_kijensen[2] and sar_kijensen[3] > 0 >=
            sar_kijensen[4]):
        print('condition Buy: True')
        return True
    else:
        print('condition Buy: False')
        return False


def condition_sale(symbol, last_tread, sar):
    query = ExitAndEnterFactor.objects.all()
    profit_coefficient = query[0].profit_coefficient
    limit_coefficient = query[0].limit_coefficient
    profit_coefficient = float(profit_coefficient) / 100 + 1
    limit_coefficient = float(limit_coefficient) / 100 + 1
    bid, ask = get_bid_ask(symbol)
    print(last_tread)
    if (last_tread['info']['side'] == 'buy'):
        if (ask / float(last_tread['info']['funds']) > profit_coefficient and ask / float(
                last_tread['info']['funds']) < limit_coefficient):
            print('condition_sale: True')
            return True
        # if (sar[0] > sar[1]):
        #     print('condition_sale: True')
        #     return True
    print('condition_sale: False')
    return False


def get_last_tread(symbol):
    try:
        today = datetime.datetime.now()
        delta = datetime.timedelta(days=20)
        day = today - delta
        data = exchange.fetch_my_trades(symbol=symbol, since=int(day.timestamp() * 1000), limit=100)
        data = data[::-1]
        return {"status": True, "data": data[0]}
    except:
        return {"status": False}
