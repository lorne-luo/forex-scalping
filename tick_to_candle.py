import csv
import sys
from datetime import datetime
from decimal import Decimal

from lib.candle import get_candle_time
from lib.constants import *


candle_dict = {}



def process_tick(time, bid, ask, timeframe):
    open_time = get_candle_time(time, timeframe)
    price = (bid + ask) / 2
    if open_time in candle_dict:
        candle = candle_dict.get(open_time)
        candle['close'] = price
        if price > candle['high']:
            candle['high'] = price
        if price < candle['low']:
            candle['low'] = price
        candle_dict[open_time] = candle
        if time < candle['open_time']:
            candle['open'] = price
        if time > candle['close_time']:
            candle['close'] = price
    else:
        # YYYY.MM.DD HH:MM O H L C V
        candle = {'open': price, 'high': price, 'low': price, 'close': price, 'open_time': time, 'close_time': time}
        candle_dict[open_time] = candle


def write_to_csv(dest):
    with open(dest, 'w') as handle:
        for key, value in candle_dict.items():
            time = key.strftime('%Y.%m.%d %H:%M')
            line = '%s,%s,%s,%s,%s\n' % (time,
                                         "{:.6f}".format(value['open']),
                                         "{:.6f}".format(value['high']),
                                         "{:.6f}".format(value['low']),
                                         "{:.6f}".format(value['close']))
            handle.write(line)


def tick_to_candle(symbol, src, timeframe):
    if timeframe not in PERIOD_CHOICES:
        raise Exception('period not correct')

    with open(src) as src_file:
        reader = csv.reader(src_file)
        for _, time, bid, ask in reader:
            time = datetime.strptime(time, '%Y%m%d %H:%M:%S.%f')
            bid = Decimal(bid)
            ask = Decimal(ask)
            process_tick(time, bid, ask, timeframe)

    dest = 'data/%s_%s.csv' % (symbol, timeframe)
    write_to_csv(dest)
    print('Output: %s' % dest)


# GBP/USD,20181202 22:01:01.100,1.27211,1.27656
# GBP/USD,20181202 22:01:05.765,1.27229,1.27674
# GBP/USD,20181202 22:01:13.455,1.27263,1.27692
# GBP/USD,20181202 22:01:13.510,1.2733,1.2752
if __name__ == "__main__":
    tick_to_candle('GBPUSD',
                   'data/GBPUSD-2018-12-tick.csv',
                   PERIOD_H1)
