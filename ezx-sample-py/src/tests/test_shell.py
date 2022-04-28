'''
Created on 15 Mar 2022

@author: shalomshachne
'''
import unittest
from tests.mocks import MockClient
import api_shell
import api_functions


class TestApiShell(unittest.TestCase):

    def setUp(self):
        self.client = MockClient()
        api_functions.client = self.client        
        self.shell = api_shell.ApiCommands()

    def test_send_new(self):
        args = 'B BAC 100 20.30'
        self.shell.do_new(args)
        self.assertEqual(1, len(self.client), "sent order")
        req = self.client.first()
        self.assertEqual(100, req.orderQty, 'set correct qty')
        self.assertEqual(20.30, req.price, 'set correct price')

    def test_send_new_with_named_properties(self):
        args = 'B BAC 100 20.30 account=EZXZXE1'
        self.shell.do_new(args)
        req = self.client.first()
        self.assertEqual(100, req.orderQty, 'set correct qty')
        self.assertEqual(20.30, req.price, 'set correct price')
        self.assertEqual('EZXZXE1', req.account, 'set account')
        


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_send_new']
    unittest.main()
