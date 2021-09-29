from binanceWrapper.utils import _makeRequest, API_PATH

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

def symbolLastKlines(symbol : str, interval, limit : int = 500):
    """
    Last (500) price bars
    TIME
    OPEN
    HIGH
    LOW
    CLOSE
    VOLUMEN
    """
    path = "/api/v3/klines"
    keyload = {
        'symbol' : symbol,
        'interval' : interval,
        'limit' : limit
    }
    return _makeRequest('GET', f"{API_PATH}{path}", params=keyload)        

def server_time():
    path = "/api/v3/time"
        
    return _makeRequest('GET', f"{API_PATH}{path}")