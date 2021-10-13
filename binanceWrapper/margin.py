import hashlib, hmac, time
from binanceWrapper import Keys, _makeRequest, API_PATH


def marginAccount():
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
        'X-MBX-APIKEY': Keys.API.get(),
    }

    def params():
        curr_time = int(time.time()*1000)
        msg = f'timestamp={curr_time}'
        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(msg), 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()

        return {
            'timestamp': curr_time,
            'signature': sig
        }

    return _makeRequest('GET', f"{API_PATH}{path}", params=params, headers=headers)

def marginNewOrder(symbol, side, quantity = 0, quoteOrderQty = 0, sideEffectType = None):
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
        'X-MBX-APIKEY': Keys.API.get(),
    }

    def params():
        nonlocal msg, payload
        curr_time = int(time.time()*1000)
        timeMsg = msg + f"&timestamp={curr_time}"

        #signature message
        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(timeMsg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        payload['timestamp'] = curr_time
        payload['signature'] = sig

        return payload
        
    return _makeRequest('POST', f"{API_PATH}{path}", params= params, headers=headers)


def borrowAvailable(asset, ):
    path = "/sapi/v1/margin/maxBorrowable"
    msg = f"asset={asset}"
    payload = {
        'asset' : asset
    }

    headers = {
        'X-MBX-APIKEY': Keys.API.get(),
    }

    def params():
        nonlocal payload, msg
        curr_time = int(time.time()*1000)
        timeMsg = msg + f'&timestamp={curr_time}'
        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(timeMsg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        payload['timestamp'] = curr_time
        payload['signature'] = sig
        return payload

    return _makeRequest('GET', f"{API_PATH}{path}", params= params, headers=headers)

def marginRepay(asset, qty, ):
    path = "/sapi/v1/margin/repay"

    msg = f'asset={asset}&amount={qty}'

    payload = {
        'asset': asset,
        'amount': qty,
    }

    headers = {
        'X-MBX-APIKEY': Keys.API.get(),
    }

    def params():
        nonlocal payload, msg
        curr_time = int(time.time()*1000)
        timeMsg = msg + f"&timestamp={curr_time}"

        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(timeMsg), 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()

        payload['timestamp'] = curr_time
        payload['signature'] = sig

        return payload

    return _makeRequest('POST', f"{API_PATH}{path}", params=params, headers=headers)


def exchangeInfo(symbol=None, symbols=None):
    path = '/api/v3/exchangeInfo'

    if symbol != None:
        params = {'symbol': symbol}
    elif symbols != None:
        msg = '['
        for i, sym in enumerate(symbols):
            if i < len(symbols)-1:
                msg += f'"{sym}",'
            else:
                msg += f'"{sym}"]'

        params = {'symbols': msg}

    return _makeRequest('GET', f"{API_PATH}{path}", params=params)


#-------------------------------------------------- UTILS

def maxTradable(asset):
    """
    returns the free amount of asset and borrow available of asset
    """
    margin_acc = marginAccount()['userAssets']

    maxBorrow = borrowAvailable(asset)
    assetInfo = next(x for x in margin_acc if x['asset'] == asset)
    return [assetInfo['free'], maxBorrow['amount']]


def marginPaySingleAsset(asset):
    """
    asset -> string; asset name
    """
    margin_acc = marginAccount()['userAssets']

    asset = next(_asset for _asset in margin_acc if _asset['asset'] == asset)

    if float(asset['free']) >= float(asset['borrowed']) > 0:
        marginRepay(asset['asset'], asset['borrowed'])


def payInterest(asset='BNB'):
    """
    asset -> string; default 'BNB'.
    """
    try:
        margin_acc = marginAccount()['userAssets']
    except KeyError:
        return
    asset_information = next(
        _asset for _asset in margin_acc if _asset['asset'] == asset)
    if float(asset_information['free']) >= float(asset_information['interest']) > 0:
        marginRepay(asset_information['asset'], asset_information['interest'])


def payDebts(asset=None):
    if asset:
        return marginPaySingleAsset(asset)

    assets = marginAccount()['userAssets']
    for asset in assets:
        if asset['borrowed'] == '0':
            continue
        elif asset['free'] != '0':
            if float(asset['free']) >= float(asset['borrowed']) > 0:
                marginRepay(asset['asset'], asset['borrowed'])


def marginBalance():
	from binanceWrapper.info import symbolPrice
	marginAcc = marginAccount()
	btcPrice = symbolPrice('BTCUSDT')
	return round(float(btcPrice['price']) * float(marginAcc['totalNetAssetOfBtc']), 2)
