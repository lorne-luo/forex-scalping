import csv
from datetime import datetime

PERIOD_M1 = 1
PERIOD_M5 = 5
PERIOD_M15 = 15
PERIOD_M30 = 30
PERIOD_H1 = 60
PERIOD_H4 = 240
PERIOD_D1 = 1440
PERIOD_W1 = 10080
PERIOD_MN1 = 43200

PERIOD_CHOICES = [PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1]

candle_dict = {}


def tick_to_candle(src, dest, timeframe):
    if timeframe not in PERIOD_CHOICES:
        raise Exception('period not correct')

    with open(src) as src_file:
        reader = csv.reader(src_file)
        for symbol, time, bid, ask in reader:
            time = datetime.strptime(time, '%Y%m%d %H:%M:%S.%f')
            process_tick(symbol, time, bid, ask)


def process_tick(symbol, time, bid, ask):
    pass


def get_candle_time(time, timeframe):
    t = time.replace(second=0, microsecond=0)

    if timeframe in [PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30]:
        minute = t.minute // timeframe * timeframe
        return t.replace(minute=minute)
    if timeframe in [PERIOD_H1, PERIOD_H4]:
        t = t.replace(minute=0)
        hourframe = int(timeframe / 60)
        hour = t.hour // hourframe * hourframe
        return t.replace(hour=hour)
    if timeframe in [PERIOD_D1]:
        return t.replace(hour=0, minute=0)

    raise NotImplementedError
