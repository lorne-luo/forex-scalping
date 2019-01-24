import numpy as np
import pandas as pd
import urllib
from time import mktime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
from constants import *


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def dateb2num(b, encoding='utf-8'):
    s = b.decode(encoding)
    strconverter = mdates.strpdate2num('%Y.%m.%d %H:%M')
    return strconverter(s)


def get_time_width(timeframe):
    now = datetime.now()
    time_width = mdates.date2num(now) - mdates.date2num(now - timedelta(minutes=5))
    return time_width*.8


def graph_data(file, symbol, timeframe):
    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    # Unfortunately, Yahoo's API is no longer available
    # feel free to adapt the code to another source, or use this drop-in replacement.
    with open(file) as f:
        date, openp, high, low, close = np.loadtxt(f,
                                                   delimiter=',',
                                                   unpack=True,
                                                   converters={0: dateb2num})

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        append_me = date[x], openp[x], high[x], low[x], close[x], 0
        ohlc.append(append_me)
        x += 1

    time_width = get_time_width(timeframe)
    print(time_width)
    candlestick_ohlc(ax1, ohlc, width=time_width, colorup='#77d879', colordown='#db3f3f')

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(90)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d %H:%M'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(1))
    ax1.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(symbol)
    plt.legend()
    plt.subplots_adjust(left=0.15, bottom=0.3, right=0.94, top=0.90, wspace=0, hspace=0)
    plt.show()


graph_data('GBPUSD_5.csv', 'GBPUSD', PERIOD_M5)

