import requests, json, logging
from binanceWrapper.exceptions import *
API_PATH = "https://api.binance.com"


def ping():
    path = "/api/v3/ping"
    timeout = 5
    while True:
        try:
            req = requests.get(f"{API_PATH}{path}", timeout=timeout)
            if req.status_code == 200:
                return True
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            continue


def _makeRequest(method: str, url: str, params=None, **kwargs):
  """
  makes the request and check/validates any errors

  method : str
  url : str
  params : dict
  header : dict
  """
  call = None
  if callable(params):
      call = params
  while True:
      try:
          if callable(call):
            params = call()
          response = requests.request(method, url, params=params, **kwargs)

          if response.status_code == 200:
              return response.json()
          else:
              return _requestError(response, response.json()['code'], params)

      except requests.Timeout:
          continue
      except requests.ConnectionError:
          logging.error(f"connection error")
          raise ConnectionError

def _requestError(response, code, params):
  if code == -3007 or code == -1021:
      raise requests.Timeout
  elif code == -3015:
      logging.error(response.text + f"\n      params : {json.dumps(params)}\n", stack_info=True)
      raise RepayExceedsBorrow
  elif code == -2010:
      logging.error(response.text + f"\n      params : {json.dumps(params)}\n", stack_info=True)
      raise InsuficientBalance
  elif code == -3006:
      # logging.error(response.text + f"\n      params : {json.dumps(params)}\n    max tradable : {json.dumps(max_tradable('USDT'))}\n", stack_info=True)
      raise WrapperError
  else :
      logging.error(response.text + f"\n      params : {json.dumps(params)}\n", stack_info=True)
      raise WrapperError
