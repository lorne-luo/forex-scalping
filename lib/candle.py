from .constants import *


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