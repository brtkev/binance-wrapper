import hashlib, hmac, time
from binanceWrapper import Keys, _makeRequest, API_PATH, utils

def newOCO(**kwargs) -> dict:
    """
    Kwargs:
        symbol (str): symbol name
        listClientOrderId (Optional[str]): A unique Id for the entire orderList
        side (enum): 'BUY' 'SELL'
        quantity (float): 
        limitClientOrderId (Optional[str]): A unique Id for the limit order
        price (float):
        limitIcebergQty (Optional[float]):
        stopClientOrderId (Optional[str]):
        stopPrice (float):
        stopLimitPrice (Optional[float]):
        stopIcebergQty (Optional[float]):
        stopLimitTimeInForce (Optional[enum]): 'GTC' 'FOK' 'IOC'
        newOrderRespType (Optional[enum]): Set the response JSON
        recvWindow (Optional[float]): The value cannot be greater than 60000
        timestamp (int):

    Price Restrictions:
        SELL: Limit Price > Last Price > Stop Price
        BUY: Limit Price < Last Price < Stop Price
    Quantity Restrictions:
        Both legs must have the same quantity
        ICEBERG quantities however do not have to be the same.
    Order Rate Limit
        OCO counts as 2 orders against the order rate limit.
    """
    payload = {
        'symbol' : kwargs['symbol'],
        'side' : kwargs['side'],
        # 'quantity' : kwargs['quantity'],
        # 'limitClientOrderId' : kwargs['limitClientOrderId'],
        # 'price' : kwargs['price'],
        # 'limitIcebergQty' : kwargs['limitIcebergQty'],
        # 'stopClientOrderId' : kwargs['stopClientOrderId'],
        # 'stopPrice' : kwargs['stopPrice'],
        # 'stopLimitPrice': kwargs['stopLimitPrice'],
        # 'stopIcebergQty': kwargs['stopIcebergQty'],
        # 'stopLimitTimeInForce': kwargs['stopLimitTimeInForce'],
        # 'newOrderRespType' : kwargs['newOrderRespType'],
        # 'recvWindow' : kwargs['recvWindow'],
        # 'timestamp' : kwargs['timestamp']
    }
    utils.optionalKey(payload, kwargs, 'listClientOrderId')

    pass
