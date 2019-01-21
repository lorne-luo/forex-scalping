import requests
import csv
from io import StringIO
from datetime import datetime
from pprint import pprint
from decimal import Decimal

USERNAME = QUALIFIER = 'luotao'
PASSWORD = 'lt1116'
SESSION_ID = ''

SESSION_URL = 'http://webrates.truefx.com/rates/connect.html?u=%s&p=%s&q=%s' % (USERNAME, PASSWORD, QUALIFIER)
API_URL = SESSION_URL + '&id=%s&f=csv'


def get_session_id():
    r = requests.get(SESSION_URL)
    return r.text.strip()


def request_api():
    global SESSION_ID
    if not SESSION_ID:
        SESSION_ID = get_session_id()

    url = API_URL % SESSION_ID
    r = requests.get(url)
    return r.text


def get_quote():
    data = request_api().strip()
    reader = csv.reader(StringIO(data))
    result = {}
    for symbol, timestamp, bid_big, bid_point, ask_big, ask_point, high, low, mean in reader:
        time = datetime.utcfromtimestamp(int(timestamp) / 1000)
        bid = Decimal(bid_big + bid_point)
        ask = Decimal(ask_big + ask_point)
        result.update({symbol: [time, bid, ask]})

    pprint(result)
    return result


get_quote()
