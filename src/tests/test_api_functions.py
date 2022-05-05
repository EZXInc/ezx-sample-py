'''
Created on 10 Mar 2022

@author: shalomshachne
'''

from Tools.scripts.nm2def import symbols
from threading import _counter
import unittest

from pip._internal import req

import api_functions
from iserver import util
import iserver
from iserver.EzxMsg import EzxMsg
from iserver.enums.msgenums import Side, OrdType, MsgType
from iserver.msgs.OrderRequest import OrderRequest
from iserver.msgs.OrderResponse import OrderResponse
from iserver.net import ApiClient
from tests import test_data_factory
from tests.mocks import MockClient
from tests.test_data_factory import *
from iserver.msgs.Reject import Reject


class ApiFunctionsTest(unittest.TestCase):

    _counter = 1
    
    def nextNumber(self): 
        ApiFunctionsTest._counter = ApiFunctionsTest._counter + 1
        return ApiFunctionsTest._counter

    def setUp(self):
        self.mock_client = MockClient()
        api_functions.client = self.mock_client

    def test_parse_side(self):
        expected = Side.BUY.value
        actual = api_functions.parse_side('B')
        self.assertEqual(expected, actual)
        
    def test_data_factory_conn_info(self):
        info = test_data_factory.create_connection_info()
        self.assertEqual('localhost', info.host)
    
    def test_send_new_sends_orderRequest(self):
        symbol = random_symbol()
        qty = random_quantity()
        price = random_price()
        side = 'S'
        api_functions.send_new_order(side, symbol, qty, price)
        
        req = self.mock_client.sent[0]
        self.assertIsInstance(req, OrderRequest, "sent an orderreqest")
        field = 'symbol'
        self.assertEqual(symbol, req.symbol, field)
        self.assertEqual(qty, req.orderQty, 'qty')
        self.assertEqual(price, req.price, 'price')
        self.assertEqual(api_functions.destination, req.destination, 'dest')
        
        myId = req.myID
        self.assertIsNotNone(myId)
        self.assertEqual(req, api_functions.pending_orders.get(myId), 'cached pending order')
        
    def test_send_new_sends_ordType(self):
        symbol = random_symbol()
        qty = random_quantity()
        price = random_price()
        side = 'S'
        api_functions.send_new_order(side, symbol, qty, price)
        
        req = self.mock_client.sent[0]
        field = 'ordType'
        self.assertEqual(OrdType.LIMIT.value, req.ordType, field)
        

    def send_new_order(self):
        symbol = random_symbol()
        qty = random_quantity()
        price = 0
        side = 'S'
        api_functions.send_new_order(side, symbol, qty, price)
        req = self.mock_client.sent[0]
        return req

    def test_send_new_sends_market_order(self):
        req = self.send_new_order()
        field = 'ordType'
        self.assertEqual(OrdType.MARKET.value, req.ordType, field)        
        
        
    def test_stores_order_response(self):
        self.test_send_new_sends_orderRequest()
        req = next(iter(api_functions.pending_orders.values()))
        response = OrderResponse(myID=req.myID, routerOrderID=self.nextNumber())
        print(f'response={response}')
        
        api_functions.msg_handler(response.msg_subtype, response)
        
        self.assertEqual(response, api_functions.open_orders.get(response.routerOrderID), 'cached response by orderID')
        self.assertIsNone(api_functions.pending_orders.get(req.myID), 'removed the pending order')
        
    def test_kwargs(self):
        args = {'second': 2, 'third': 3}
        result = function1(1, **args)
        self.assertEqual(6, result)
        
    def test_send_order_with_named_args(self):
        symbol = random_symbol()
        qty = random_quantity()
        price = random_price()
        side = 'S'
        others = iserver.parse_to_dict('account=EZXXZE10, text=+B.1.a.4', ',')
        api_functions.send_new_order(side, symbol, qty, price, **others)
        req = self.mock_client.sent[0]
        self.assertEqual('EZXXZE10', req.account, 'account')
        self.assertEqual('+B.1.a.4', req.text, 'text')
        
    def test_reject_removes_order(self):
        req = self.send_new_order()
        self.assertTrue(api_functions.get_pending_order(req.myID))
        reject = Reject(msgType = MsgType.NEW, myID=req.myID)
        api_functions.msg_handler(reject.msg_subtype, reject)
        
        self.assertFalse(api_functions.get_pending_order(req.myID), 'removed pending order foe NEW reject')
        
        
    
def function1(first, second, third):
    return first + second + third


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_parse_side']
    unittest.main()
