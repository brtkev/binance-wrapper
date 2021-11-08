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
        self.queryOCO(res['orderListId'])
        self.cancelOCO(res['orderListId'])

    def cancelOCO(self, orderListId):
        binanceWrapper.cancelOCO(symbol = 'BTCBUSD', orderListId=orderListId)


    def queryOCO(self, orderListId):
        binanceWrapper.queryOCO(orderListId=orderListId)                        
    
    def queryAllOCO(self):
        binanceWrapper.queryAllOCO()