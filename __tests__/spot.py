import binanceWrapper, os
import unittest
from dotenv import load_dotenv

class Spot(unittest.TestCase):
    pass

    def setUp(self) -> None:
        load_dotenv()
        binanceWrapper.setKeys(os.getenv('APIKEY'), os.getenv('SECRETKEY'))

    def newOCO(self) -> None:
        price = float(binanceWrapper.symbolPrice('BTCBUSD')['price'])
        takePrice = round(price + price * 0.1, 2)
        lossPrice = round(price - price * 0.1, 2)
        qty = round(10/price, 4)
        res = binanceWrapper.newOCO(symbol = 'BTCBUSD', side = 'SELL', quantity=qty, price=takePrice,
        stopPrice=lossPrice+10, stopLimitPrice=lossPrice, stopLimitTimeInForce= 'FOK')
        print(res)

    def cancelOCO(self):
#         a = {'symbol': 'BTCBUSD', 'side': 'SELL', 'quantity': 0.0002, 'price': 67161.36, 'stopPrice': 54960.2, 'stopLimitPrice': 54950.2, 'stopLimitTimeInForce': 'FOK', 'timestamp': 1636170208897, 'signature': '6C21C2844BCABD51B61278B06B7D1F21372A16D2E8FEDEEBABBE13169A081A71'}
# {'orderListId': 50697883, 'contingencyType': 'OCO', 'listStatusType': 'EXEC_STARTED', 'listOrderStatus': 'EXECUTING', 'listClientOrderId': 'p7ZHGqfOoJDE8d9eoxPxtu', 'transactionTime': 1636170209113, 'symbol': 'BTCBUSD', 'orders': [{'symbol': 'BTCBUSD', 'orderId': 3659813675, 'clientOrderId': '4A3FyugpaMj7oos1zQqmOb'}, {'symbol': 'BTCBUSD', 'orderId': 3659813676, 'clientOrderId': 'Y6mgc6wu1G9w3hANE9wKww'}], 'orderReports': [{'symbol': 'BTCBUSD', 'orderId': 3659813675, 'orderListId': 50697883, 'clientOrderId': '4A3FyugpaMj7oos1zQqmOb',
# 'transactTime': 1636170209113, 'price': '54950.20000000', 'origQty': '0.00020000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'FOK', 'type': 'STOP_LOSS_LIMIT', 'side': 'SELL', 'stopPrice': '54960.20000000'}, {'symbol': 'BTCBUSD', 'orderId': 3659813676, 'orderListId': 50697883, 'clientOrderId': 'Y6mgc6wu1G9w3hANE9wKww', 'transactTime': 1636170209113, 'price': '67161.36000000', 'origQty': '0.00020000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT_MAKER', 'side': 'SELL'}]}
        print(
            binanceWrapper.cancelOCO(symbol = 'BTCBUSD', listClientOrderId='p7ZHGqfOoJDE8d9eoxPxtu')
        )


    def queryOCO(self):
        print(
            binanceWrapper.queryOCO(orderListId=50697883)
        )                                       
    
    