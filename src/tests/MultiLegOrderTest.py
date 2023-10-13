'''
Created on 11 Oct 2023

@author: shalomshachne
'''
import unittest

from iserver.enums.msgenums import Side, CFICode, MsgType
from orders import MultiLegOrder, EquityLegOrder, OptionLegOrder
from tests.test_data_factory import random_symbol, random_price, random_quantity
from iserver import ezx_msg

DEFAULT_DESTINATION = 'SIMU'
DEFAULT_ACCOUNT = 'ACCOUNT1'


class Test(unittest.TestCase):

    def setUp(self):
        self.order = MultiLegOrder(-2.34, 5, DEFAULT_DESTINATION, DEFAULT_ACCOUNT)
        
    def testConstructor(self):
        self.order = MultiLegOrder(-2.34, 5, DEFAULT_DESTINATION, DEFAULT_ACCOUNT)
        self.assertEqual(self.order.destination, DEFAULT_DESTINATION, 'destination set')
        self.assertEqual(self.order.account, DEFAULT_ACCOUNT, 'account set')
        self.assertEquals(self.order.price, -2.34, "price")
        self.assertEquals(self.order.orderQty, 5, "orderQty")        
        
    def testConstructorNegativePriceSetsSideSell(self):
        self.order = MultiLegOrder(-2.34, 5, DEFAULT_DESTINATION, DEFAULT_ACCOUNT)
        self.assertEquals(self.order.side, 2, "negative price sets side sell")
        
    def testConstructorPositivePriceSetsSideBuy(self):
        self.order = MultiLegOrder(0, 5, DEFAULT_DESTINATION, DEFAULT_ACCOUNT)
        self.assertEquals(self.order.side, 1, "positive price sets side sell")                

        self.order = MultiLegOrder(.50, 5, DEFAULT_DESTINATION, DEFAULT_ACCOUNT)
        self.assertEquals(self.order.side, 1, "positive price sets side sell")                

    def testDefaultValues(self): 
        order = self.order
        self.assertEqual('MLEG', order.securityType, "securityType")
        self.assertEqual('NA', order.symbol, 'symbol')
        print(f'msgType={MsgType}')        
        expected = MsgType.NEW.value
        actual = order.msgType
        self.assertEquals(expected, actual, 'msgType to NEW')
        
    def testAddLegs(self):
        order = self.order
        order.destination = 'EROOM'        
        leg1 = EquityLegOrder('MSFT', Side.BUY, 1)
        order.add_leg(leg1);
        
        self.assertEqual(1, len(order.legList), 'added leg')
        
        read = order.get_leg(0)
        self.assertEqual(leg1, read)
        
    def testEquityLeg(self):
        leg = EquityLegOrder('MSFT', Side.SELL, 3)
        self.assertEquals(3, leg.ratioQty)
        self.assertEquals('MSFT', leg.symbol)
        self.assertEquals(2, leg.side)
        self.assertEquals('CS', leg.securityType)        
        
    def testOptionLeg(self):
        symbol = random_symbol()
        side = Side.SELL
        ratioQty = random_quantity()
        cfiCode = CFICode.OPTION_CALL
        strikePrice = random_price()
        maturityDate = '20231215'
        
        leg = OptionLegOrder(symbol, side, ratioQty, cfiCode, strikePrice, maturityDate)
        test = self.assertEqual
        test(symbol, leg.symbol)
        
        test(side.value, leg.side, 'side')
        test(ratioQty, leg.ratioQty, 'ratioQty')
        test('OC', leg.cfiCode, 'cfiCode')
        test(strikePrice, leg.strikePx, 'strikePrice')
        test('202312', leg.maturityMonthYear, 'maturityMonthYear')
        test(15, leg.maturityDay)
        test('OPT', leg.securityType)
     
    def testEncode(self):
        parentQty = random_quantity(10, 100)
        parentPrice = random_price(1.00, 30) * -1
        order = MultiLegOrder(parentPrice, parentQty, DEFAULT_DESTINATION, DEFAULT_ACCOUNT)
        
        # leg values
        symbol = random_symbol()
        side = Side.SELL
        ratioQty1 = random_quantity(1, 3)
        ratioQty2 = random_quantity(1, 3)
        cfiCode = CFICode.OPTION_CALL
        strikePrice = random_price()
        maturityDate = '20231215'        
        
        order.add_leg(EquityLegOrder(symbol, side, ratioQty1))
        order.add_leg(OptionLegOrder(symbol, side, ratioQty2, cfiCode, strikePrice, maturityDate))
        
        msg = ezx_msg.to_api_msg(order)  
        msg = msg.replace(ezx_msg.TAG_VALUE_PAIRS_DELIMITER, '|')
              
        print(msg)
        self.assertTrue('SECTYPE=OPT' in msg)
        self.assertTrue('SECTYPE=CS' in msg)
        self.assertTrue('STRIKEPX' in msg)
 
    def testMlegCtorWithKwargs(self):
        userInfo = 'some information'
        self.order = MultiLegOrder(-2.34, 5, DEFAULT_DESTINATION, DEFAULT_ACCOUNT, userInfo=userInfo, currency='USD')
        self.assertEquals(userInfo, self.order.userInfo, 'set userInfo')
        self.assertEquals('USD', self.order.currency, 'set userInfo')
        
    def testEquityLegWithKwargs(self):
        exDest = 'NYSE'
        lastPrice = 10.20
        leg = EquityLegOrder('MSFT', Side.SELL, 3, exDest=exDest, lastPrice=lastPrice)
        self.assertEquals(exDest, leg.exDest, 'set exDest')
        self.assertEquals(lastPrice, leg.lastPrice, 'set lastPrice')
        
    def testOptionLegWithKwargs(self):
        exDest = 'NYSE'
        lastPrice = 10.20
        leg = OptionLegOrder('MSFT', Side.SELL, 3, CFICode.OPTION_PUT, 10.20, '20240128',  exDest=exDest, lastPrice=lastPrice)
        self.assertEquals(exDest, leg.exDest, 'set exDest')
        self.assertEquals(lastPrice, leg.lastPrice, 'set lastPrice')        
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testDefaultValues']
    unittest.main()
