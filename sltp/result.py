import os
import csv
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from math import fabs

from lib.candle import get_candle_time
from lib.constants import PERIOD_M5

tick_csv = 'data/GBPUSD-2018-12-tick.csv'


def get_pip(value, places=4, abs=True):
    value = value * 10000
    if abs:
        value = fabs(value)
    format = "{0:.%sf}" % places
    return float(format.format(value))


def parse_row(data):
    symbol = data[0]
    time = datetime.strptime(data[1], '%Y%m%d %H:%M:%S.%f')
    bid = Decimal(data[2])
    ask = Decimal(data[3])
    return symbol, time, bid, ask


def max_profit(index, current_time, current_bid, current_ask, data, delta):
    max_sell = max_buy = max_sell_interval = max_buy_interval = 0
    for i in range(index + 1, len(data)):
        symbol, time, bid, ask = parse_row(data[i])
        time_interval = time - current_time
        if time_interval > delta:
            # print(time, bid, ask)
            # print(current_time, current_bid, current_ask)
            max_sell = get_pip(max_sell)
            max_buy = get_pip(max_buy)
            # print(max_sell, max_buy, max_sell_interval, max_buy_interval)
            return max_sell, max_buy, max_sell_interval, max_buy_interval

        # print(current_bid, ask, current_bid - ask)
        # print(current_ask, bid, bid - current_ask)

        if current_bid - ask > max_sell:
            # print('down')
            max_sell = current_bid - ask
            # print(current_bid, ask)
            max_sell_interval = int(time_interval.seconds / 60)

        if bid - current_ask > max_buy:
            # print('up',ask - current_ask)
            max_buy = bid - current_ask
            # print(current_ask, bid)
            max_buy_interval = int(time_interval.seconds / 60)
    return get_pip(max_sell), get_pip(max_buy), max_sell_interval, max_buy_interval


if __name__ == "__main__":
    print('start')
    timeframe = PERIOD_M5

    with open(tick_csv) as tick:
        data = csv.reader(tick)
        data = list(data)

        stat_data = {}
        count = 0
        now = datetime.now()
        for index, row in enumerate(data):
            symbol, time, bid, ask = parse_row(row)
            candle_time = get_candle_time(time, timeframe)

            if candle_time not in stat_data:
                max_sell, max_buy, max_sell_interval, max_buy_interval = max_profit(index, time, bid, ask, data,
                                                                                    timedelta(minutes=45))
                stat_data[candle_time] = ([candle_time, max_sell, max_buy, max_sell_interval, max_buy_interval])
            else:
                continue

            count += 1
            if not count % 1000:
                print(count, (datetime.now() - now).seconds)
            # if count == 1000:
            #     break
        print('#1 process csv spend %s seconds.' % (datetime.now() - now).seconds)
        now = datetime.now()

    data = [v for k, v in stat_data.items()]
    df = pd.DataFrame(data, columns=['time', 'max_sell', 'max_buy', 'max_sell_interval', 'max_buy_interval'])
    df = df.set_index('time')
    df.to_csv('GBPUSD_tick_result.csv')
    print('#2 save csv spend %s seconds.' % (datetime.now() - now).seconds)
