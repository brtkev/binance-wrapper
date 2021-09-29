import requests, time, hmac, hashlib, os, signal, logging, traceback, json
# import private.keys as keys
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

def make_request(method : str, url : str, params=None,**kwargs):
    """
    makes the request and check/validates any errors

    method : str
    url : str
    params : dict
    header : dict
    """
    if callable(params):
        call = params
    while True :
        try:
                
            try:
                params = call()
            except NameError:
                pass
            
            response = requests.request(method, url, params=params, **kwargs)

            if response.status_code == 200:
                return response.json()
            else:
                errorCode = response.json()['code']
                if errorCode == -3007 or errorCode == -1021:
                    raise requests.Timeout
                elif errorCode == -3015:
                    logging.error(response.text + f"\n      params : {json.dumps(params)}\n", stack_info=True)
                    return RepayExceedsBorrow
                elif errorCode == -2010:
                    logging.error(response.text + f"\n      params : {json.dumps(params)}\n", stack_info=True)
                    raise InsuficientBalance
                elif errorCode == -3006:
                    logging.error(response.text + f"\n      params : {json.dumps(params)}\n    max tradable : {json.dumps(max_tradable('USDT'))}\n", stack_info=True)
                    raise WrapperError
                else:
                    logging.error(response.text + f"\n      params : {json.dumps(params)}\n", stack_info=True)
                    raise WrapperError
        except requests.Timeout:
            continue
        except requests.ConnectionError:
            logging.error(f"connection error")
            raise ConnectionError


def symbol_price( symbol = ''):
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

    return make_request('GET', f"{API_PATH}{path}", params = keyload)
        


def symbol_last_klines(symbol : str, interval, limit : int = 500):
    path = "/api/v3/klines"
    keyload = {
        'symbol' : symbol,
        'interval' : interval,
        'limit' : limit
    }


    return make_request('GET', f"{API_PATH}{path}", params=keyload)        
    
def server_time():
    path = "/api/v3/time"
        
    return make_request('GET', f"{API_PATH}{path}")
    
    

def account_coins():
    path = "/sapi/v1/capital/config/getall"

    headers = {
        'X-MBX-APIKEY': keys.API,
    }


    def params():
        curr_time = int(time.time()*1000)
        msg = f'timestamp={curr_time}'
        sig = hmac.new(
            bytes(keys.SECRET, 'latin-1'),
            msg=bytes(str(msg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        return {
            'timestamp' : curr_time,
            'signature' : sig
        }


    return make_request('GET', f"{API_PATH}{path}", params=params, headers=headers)
    

def account_info():
    path = "/api/v3/account"

    headers = {
        'X-MBX-APIKEY': keys.API,
    }

    def params():
        curr_time = int(time.time()*1000)
        msg = f'timestamp={curr_time}'
        sig = hmac.new(
            bytes(keys.SECRET, 'latin-1'),
            msg=bytes(str(msg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        return {
            'timestamp' : curr_time,
            'signature' : sig
        }

    return make_request('GET', f"{API_PATH}{path}", params=params, headers=headers)

def margin_account():
    """
    response:
    {
        'tradeEnabled' : bool,
        'transferEnabled': bool,
        'borrowEnabled': bool, 
        'marginLevel': string, 
        'totalAssetOfBtc': string, 
        'totalLiabilityOfBtc': string, 
        'totalNetAssetOfBtc': string,
        'userAssets': list 
    }

    userAssets values:
    {
        'asset': 'BTC',
        'free': '0.003137',
        'locked': '0',
        'borrowed': '0',
        'interest': '0',
        'netAsset': '0.003137'
    } 
    """
    path = "/sapi/v1/margin/account"

    headers = {
        'X-MBX-APIKEY': keys.API,
    }

    def params():
        curr_time = int(time.time()*1000)
        msg = f'timestamp={curr_time}'
        sig = hmac.new(
            bytes(keys.SECRET, 'latin-1'),
            msg=bytes(str(msg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        return {
            'timestamp' : curr_time,
            'signature' : sig
        }


    return make_request('GET', f"{API_PATH}{path}", params = params, headers = headers)

def margin_new_order(symbol, side, quantity = 0, quoteOrderQty = 0, sideEffectType = None):
    """
    symbol -> pair name; example 'BTCUSDT'.

    side -> 'BUY', 'SELL'.

    quantity, quoteOrderQty -> DECIMAL; don't use both.
    
    sideEffectType -> 'NO_SIDE_EFFECT', 'MARGIN_BUY', 'AUTO_REPAY'; default 'NO_SIDE_EFFECT'.


    """
    path = "/sapi/v1/margin/order"

    msg = f"symbol={symbol}&side={side}&type=MARKET"

    payload = {
        'symbol' : symbol,
        'side' : side,
        'type' : 'MARKET'
    }

    if quantity != 0:
        msg += f"&quantity={quantity}"
        payload['quantity'] = quantity
    elif quoteOrderQty != 0:
        quoteOrderQty = round(quoteOrderQty, 2)
        msg += f"&quoteOrderQty={quoteOrderQty}"
        payload['quoteOrderQty'] = quoteOrderQty

    if sideEffectType != None:
        msg += f"&sideEffectType={sideEffectType}"
        payload['sideEffectType'] = sideEffectType

    headers = {
        'X-MBX-APIKEY': keys.API,
    }

    def params():
        nonlocal msg, payload
        curr_time = int(time.time()*1000)
        timeMsg = msg + f"&timestamp={curr_time}"

        #signature message
        sig = hmac.new(
            bytes(keys.SECRET, 'latin-1'),
            msg=bytes(str(timeMsg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        payload['timestamp'] = curr_time
        payload['signature'] = sig

        return payload
        
    return make_request('POST', f"{API_PATH}{path}", params= params, headers=headers)


def borrow_available(asset, ):
    path = "/sapi/v1/margin/maxBorrowable"
    msg = f"asset={asset}"
    payload = {
        'asset' : asset
    }

    headers = {
        'X-MBX-APIKEY': keys.API,
    }

    def params():
        nonlocal payload, msg
        curr_time = int(time.time()*1000)
        timeMsg = msg + f'&timestamp={curr_time}'
        sig = hmac.new(
            bytes(keys.SECRET, 'latin-1'),
            msg=bytes(str(timeMsg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        payload['timestamp'] = curr_time
        payload['signature'] = sig
        return payload

    return make_request('GET', f"{API_PATH}{path}", params= params, headers=headers)

def margin_borrow(asset, qty): ...
#     """
#     deprecated
#     """

#     path = "/sapi/v1/margin/loan"
#     curr_time = int(time.time()*1000)
#     msg = f'asset={asset}&amount={qty}&timestamp={curr_time}'
#     sig = hmac.new(
#         bytes(keys.SECRET, 'latin-1'),
#         msg=bytes(str(msg),'latin-1'),
#         digestmod=hashlib.sha256
#     ).hexdigest().upper()    

#     payload = {
#         'asset' : asset,
#         'amount' : qty,
#         'timestamp' : curr_time,
#         'signature' : sig
#     }

#     headers = {
#         'X-MBX-APIKEY': keys.API,
#     }

#     req = requests.post(f"{API_PATH}{path}", params= payload, headers=headers)
#     if req.status_code == 200:
#         return req.json()
#     else:
#         req = req.json()
#         print(req)
#         if req['code'] == -3006:
#             return -1
#         os.kill(os.getpid(), signal.SIGINT)


def margin_repay(asset, qty, ):
    path = "/sapi/v1/margin/repay"
    
    msg = f'asset={asset}&amount={qty}'

    payload = {
        'asset' : asset,
        'amount' : qty,
    }

    headers = {
        'X-MBX-APIKEY': keys.API,
    }

    def params():
        nonlocal payload, msg
        curr_time = int(time.time()*1000)
        timeMsg = msg + f"&timestamp={curr_time}"

        sig = hmac.new(
            bytes(keys.SECRET, 'latin-1'),
            msg=bytes(str(timeMsg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        
        payload['timestamp'] = curr_time
        payload['signature'] = sig

        return payload

    return make_request('POST', f"{API_PATH}{path}", params= params, headers=headers)

def exchange_info( symbol = None, symbols = None):
    path = '/api/v3/exchangeInfo'

    if symbol != None:
        params = {'symbol' : symbol}
    elif symbols != None:
        msg = '['
        for i, sym in enumerate(symbols):
            if i < len(symbols)-1:
                msg += f'"{sym}",'
            else:
                msg += f'"{sym}"]'

        params = { 'symbols' : msg}
    

    return make_request('GET', f"{API_PATH}{path}", params= params)


#-------------------------------------------------- UTILS

def max_tradable(asset):
    """
    returns the free amount of asset and borrow available of asset
    """
    margin_acc = margin_account()['userAssets']
    
    maxBorrow = borrow_available(asset)
    assetInfo = next( x for x in margin_acc if x['asset'] == asset)
    return [assetInfo['free'], maxBorrow['amount']]


def margin_pay_single_asset(asset):
    """
    asset -> string; asset name
    """
    margin_acc = margin_account()['userAssets']

    asset = next( _asset for _asset in margin_acc if _asset['asset'] == asset)

    if float(asset['free']) >= float(asset['borrowed']) > 0:
        margin_repay(asset['asset'], asset['borrowed'])



def pay_interest(asset = 'BNB'):
    """
    asset -> string; default 'BNB'.
    """
    try:
        margin_acc = margin_account()['userAssets']
    except KeyError:
        return
    asset_information = next( _asset for _asset in margin_acc if _asset['asset'] == asset)
    if float(asset_information['free']) >= float(asset_information['interest']) > 0:
        margin_repay(asset_information['asset'], asset_information['interest'])
        

def pay_debts(asset = None):
    if asset:
        return margin_pay_single_asset(asset)

    assets = margin_account()['userAssets']
    for asset in assets:
        if asset['borrowed'] == '0':
            continue
        elif asset['free'] != '0':
            if float(asset['free']) >= float(asset['borrowed']) > 0:
                margin_repay(asset['asset'], asset['borrowed'])

def margin_balance():
    marginAccount = margin_account()
    btcPrice = symbol_price('BTCUSDT')
    return round(float(btcPrice['price']) * float(marginAccount['totalNetAssetOfBtc']), 2)


#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
