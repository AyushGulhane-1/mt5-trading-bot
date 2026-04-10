import MetaTrader5 as mt
import pandas as pd
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os

# Initialize MT5 and login
if not mt.initialize("C:\\Program Files\\MetaTrader 5\\terminal64.exe"):
    print("Initialize failed:", mt.last_error())
    quit()

load_dotenv()

LOGIN = str(os.getenv("LOGIN"))
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")

if not mt.login(LOGIN, PASSWORD, SERVER):
    print("Login failed:", mt.last_error())
    quit()

print("Connected successfully")

ticker = 'XAUUSD'
interval = mt.TIMEFRAME_M1
qty = 0.01
sl_pct = 0.05
tp_pct = 0.1

buy_order_type = mt.ORDER_TYPE_BUY
sell_order_type = mt.ORDER_TYPE_SELL


def create_order(ticker, qty, order_type, price, sl, tp):
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": ticker,
        "volume": qty,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "comment": "Python Open Position",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_FOK,
    }
    result = mt.order_send(request)
    print(f"Order result: {result}")
    return result


def close_order(ticket, order_type, price):
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": ticker,
        "volume": qty,
        "type": order_type,
        "position": ticket,
        "price": price,
        "deviation": 10,
        "comment": "Close Position",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_FOK,
    }
    result = mt.order_send(request)
    print(f"Close result: {result}")
    return result


# Main trading loop
while True:
    # Fetch the latest price info
    tick = mt.symbol_info_tick(ticker)
    if tick is None:
        print("Failed to get tick info.")
        time.sleep(5)
        continue

    buy_price = tick.ask
    sell_price = tick.bid

    buy_sl = buy_price * (1 - sl_pct)
    buy_tp = buy_price * (1 + tp_pct)
    sell_sl = sell_price * (1 + sl_pct)
    sell_tp = sell_price * (1 - tp_pct)

    # Get latest OHLC data (last 3 minutes)
    ohlc = pd.DataFrame(mt.copy_rates_range(
        ticker, interval, datetime.now() - timedelta(minutes=3), datetime.now()))
    ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')

    if len(ohlc) < 1:
        print("Not enough data.")
        time.sleep(10)
        continue

    current_close = ohlc.iloc[-1]['close']
    last_close = ohlc.iloc[-2]['close']
    last_high = ohlc.iloc[-2]['high']
    last_low = ohlc.iloc[-2]['low']

    long_condition = current_close > last_high
    short_condition = current_close < last_close
    closelong_condition = current_close < last_close
    closeshort_condition = current_close > last_close

    positions = mt.positions_get(symbol=ticker)
    has_position = len(positions) > 0
    already_buy = False
    already_sell = False
    ticket = None

    if has_position:
        pos = positions[0]._asdict()
        ticket = pos['ticket']
        if pos['type'] == mt.POSITION_TYPE_BUY:
            already_buy = True
        elif pos['type'] == mt.POSITION_TYPE_SELL:
            already_sell = True

    # Long signal
    if long_condition:
        if not has_position:
            create_order(ticker, qty, buy_order_type, buy_price, buy_sl, buy_tp)
            print("Buy Order Placed")
        elif already_sell:
            close_order(ticket, buy_order_type, buy_price)
            time.sleep(2)
            create_order(ticker, qty, buy_order_type, buy_price, buy_sl, buy_tp)
            print("Switched to Buy")

    # Short signal
    if short_condition:
        if not has_position:
            create_order(ticker, qty, sell_order_type, sell_price, sell_sl, sell_tp)
            print("Sell Order Placed")
        elif already_buy:
            close_order(ticket, sell_order_type, sell_price)
            time.sleep(2)
            create_order(ticker, qty, sell_order_type, sell_price, sell_sl, sell_tp)
            print("Switched to Sell")

    # Close conditions
    if closelong_condition and already_buy:
        close_order(ticket, sell_order_type, sell_price)
        print("Closed Buy Position")

    if closeshort_condition and already_sell:
        close_order(ticket, buy_order_type, buy_price)
        print("Closed Sell Position")

    time.sleep(15)
