from binanceWrapper.utils import _makeRequest, API_PATH, Keys
import hashlib, hmac, time

def symbolPrice( symbol = ''):
  """
  response:
  {
      'symbol': 'BTCUSDT',
      'price': '33825.92000000'
  }
  """
  path = "/api/v3/ticker/price"

  if symbol == '':
      keyload = {}
  else:
      keyload = { 'symbol' : symbol }

  return _makeRequest('GET', f"{API_PATH}{path}", params = keyload)

def symbolLastKlines(symbol : str, interval, limit : int = None):
    """
    Kline/candlestick bars for a symbol.
    Klines are uniquely identified by their open time.
    [openTime, open, high, low, close, volumen, closeTime, ...]
    """
    return symbolKlines(symbol, interval, limit)

def symbolKlines(symbol : str, interval : str, limit : int = None, startTime : int = None, endTime : int = None):
    """
    Kline/candlestick bars for a symbol.
    Klines are uniquely identified by their open time.
    [openTime, open, high, low, close, volumen, closeTime, ...]
    """
    path = "/api/v3/klines"
    keyload = {
        'symbol' : symbol,
        'interval' : interval,
    }
    if limit : keyload['limit'] = limit
    if startTime : keyload['startTime'] = startTime
    if endTime : keyload['endTime'] = endTime

    return _makeRequest('GET', f"{API_PATH}{path}", params=keyload)


def serverTime():
    """
    response:
    {'serverTime': miliseconds}
    """
    path = "/api/v3/time"
        
    return _makeRequest('GET', f"{API_PATH}{path}")

def accountCoins():
    """
    keys : {
        API : 'your-API-Key',
        SECRET: 'your-secret-key'
        }
    """
    path = "/sapi/v1/capital/config/getall"

    headers = {
        'X-MBX-APIKEY': Keys.API.get(),
    }


    def params():
        curr_time = int(time.time()*1000)
        msg = f'timestamp={curr_time}'
        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(msg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        return {
            'timestamp' : curr_time,
            'signature' : sig
        }


    return _makeRequest('GET', f"{API_PATH}{path}", params=params, headers=headers)

def accountInfo():
    path = "/api/v3/account"

    headers = {
        'X-MBX-APIKEY': Keys.API.get(),
    }

    def params():
        curr_time = int(time.time()*1000)
        msg = f'timestamp={curr_time}'
        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(msg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        return {
            'timestamp' : curr_time,
            'signature' : sig
        }

    return _makeRequest('GET', f"{API_PATH}{path}", params=params, headers=headers)