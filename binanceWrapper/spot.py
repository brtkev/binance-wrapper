import hashlib, hmac, time
from binanceWrapper import Keys, _makeRequest, API_PATH, utils

def newOrder(symbol : str, side : str, type : str, timeInForce : str = None, quantity : float = None,
quoteOrderQty : float = None, price : float = None, newClientOrderId : str = None, stopPrice : float = None,
icebergQty : float = None, newOrderRespType : str = None, recvWindow : int = None, test : bool = False ):
    if test: path = "/api/v3/order/test"
    else: path = "/api/v3/order"
    
    payload = {
        'symbol' : symbol,
        'side' : side,
        'type' : type
    }
    if timeInForce: payload['timeInForce'] = timeInForce
    if quantity: payload['quantity'] = quantity
    elif quoteOrderQty: payload['quoteOrderQty'] = quoteOrderQty
    if price: payload['price'] = price
    if newClientOrderId: payload['newClientOrderId'] = newClientOrderId
    if stopPrice: payload['stopPrice'] = stopPrice
    if icebergQty: payload['icebergQty'] = icebergQty
    if newOrderRespType: payload['newOrderRespType'] = newOrderRespType
    if recvWindow: payload['recvWindow'] = recvWindow

    msg = utils.getMessage(payload)
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

def newOCO(symbol : str, side : str, quantity : float, price : float, stopPrice : float, 
        stopLimitPrice : float = '', **kwargs ) -> dict:
    """
    recommended to grab orderListId out of the response

    symbol (str): symbol name\n
    listClientOrderId (Optional[str]): A unique Id for the entire orderList\n
    side (enum): 'BUY' 'SELL'\n
    quantity (float): \n
    limitClientOrderId (Optional[str]): A unique Id for the limit order\n
    price (float):\n
    limitIcebergQty (Optional[float]):\n
    stopClientOrderId (Optional[str]):\n
    stopPrice (float):\n
    stopLimitPrice (Optional[float]):\n
    stopIcebergQty (Optional[float]):\n
    stopLimitTimeInForce (Optional[enum]): 'GTC' 'FOK' 'IOC'\n
    newOrderRespType (Optional[enum]): Set the response JSON\n
    recvWindow (Optional[float]): The value cannot be greater than 60000\n

    Price Restrictions:
        SELL: Limit Price > Last Price > Stop Price
        BUY: Limit Price < Last Price < Stop Price
    Quantity Restrictions:
        Both legs must have the same quantity
        ICEBERG quantities however do not have to be the same.
    Order Rate Limit
        OCO counts as 2 orders against the order rate limit.

    example newOCO(symbol = 'BTCUSDT', side = 'BUY', quantity=1, price=200, stopPrice=250, 
    stopLimitPrice=150, stopLimitTimeInForce= 'FOK')
    """
    payload = {
        'symbol' : symbol,
        'side' : side,
        'quantity' : quantity,
        'price' : price,
        'stopPrice' : stopPrice
    }
    if stopLimitPrice: payload['stopLimitPrice'] = stopLimitPrice

    payload.update(kwargs)

    path = '/api/v3/order/oco'


    msg = utils.getMessage(payload)
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


def cancelOCO(symbol : str, orderListId : int = None, listClientOrderId : str = None, recvWindow: int = None):
    payload = {
        'symbol': symbol
    }
    if orderListId: payload['orderListId'] = orderListId
    elif listClientOrderId: payload['listClientOrderId'] = listClientOrderId
    if recvWindow: payload['recvWindow'] = recvWindow
    path = '/api/v3/orderList'
    headers = {
        'X-MBX-APIKEY': Keys.API.get(),
    }
    msg = utils.getMessage(payload)
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
        
    return _makeRequest('DELETE', f"{API_PATH}{path}", params= params, headers=headers)

def queryOCO( orderListId : int = None, listClientOrderId : str = None, recvWindow: int = None):
    path = '/api/v3/orderList'
    payload = {}
    if orderListId: payload['orderListId'] = orderListId
    elif listClientOrderId: payload['listClientOrderId'] = listClientOrderId
    if recvWindow: payload['recvWindow'] = recvWindow
    path = '/api/v3/orderList'
    headers = {
        'X-MBX-APIKEY': Keys.API.get(),
    }
    msg = utils.getMessage(payload)
    def params():
        nonlocal msg, payload
        curr_time = int(time.time()*1000)
        if len(msg) > 0: timeMsg = msg + f"&timestamp={curr_time}"
        else: timeMsg = msg + f"timestamp={curr_time}"

        #signature message
        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(timeMsg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        payload['timestamp'] = curr_time
        payload['signature'] = sig
        return payload
        
    return _makeRequest('GET', f"{API_PATH}{path}", params= params, headers=headers)



def queryAllOCO( fromId : int = None, startTime : int = None, endTime : int  = None, 
limit : int = None, recvWindow: int = None):
    path = '/api/v3/allOrderList'
    payload = {}
    if fromId : payload['fromId'] = fromId
    if startTime : payload['startTime'] = startTime
    if endTime : payload['endTime'] = endTime
    if limit : payload['limit'] = limit
    if recvWindow: payload['recvWindow'] = recvWindow
    headers = {
        'X-MBX-APIKEY': Keys.API.get(),
    }
    msg = utils.getMessage(payload)
    def params():
        nonlocal msg, payload
        curr_time = int(time.time()*1000)
        if len(msg) > 0: timeMsg = msg + f"&timestamp={curr_time}"
        else: timeMsg = msg + f"timestamp={curr_time}"

        #signature message
        sig = hmac.new(
            bytes(Keys.SECRET.get(), 'latin-1'),
            msg=bytes(str(timeMsg),'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()    

        payload['timestamp'] = curr_time
        payload['signature'] = sig
        return payload
        
    return _makeRequest('GET', f"{API_PATH}{path}", params= params, headers=headers)
