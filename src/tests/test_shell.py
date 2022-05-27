'''
Created on 15 Mar 2022

@author: shalomshachne
'''
import unittest
from tests.mocks import MockClient
import api_shell
import api_functions
import argparse
from iserver.enums.msgenums import CFICode


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
        args = 'B BAC 100 20.30 account=EZXZXE1 text=+A.1.a.1'
        self.shell.do_new(args)
        req = self.client.first()
        self.assertEqual(100, req.orderQty, 'set correct qty')
        self.assertEqual(20.30, req.price, 'set correct price')
        self.assertEqual('EZXZXE1', req.account, 'set account')
        self.assertEqual('+A.1.a.1', req.text, 'set account')
        
    def test_send_option_with_named_properties(self):
        args = 'B IBM 150 3.68 -x 20220627 -s 999 -t Put  -p account=5CG05400 text=+B.1.a.4'
        self.shell.do_option(args)
        req = self.client.first()
        self.assertEqual(150, req.orderQty, 'set correct qty')
        self.assertEqual(3.68, req.price, 'set correct price')
        self.assertEqual('5CG05400', req.account, 'set account')
        self.assertEqual('+B.1.a.4', req.text, 'set account')
        
    def test_send_option_with_named_properties_and_args_after(self):
        args = 'B IBM 150 3.68 -x 20220627 -s 999 -p account=5CG05400 text=+B.1.a.4 -t Put'
        self.shell.do_option(args)
        req = self.client.first()
        self.assertEqual(150, req.orderQty, 'set correct qty')
        self.assertEqual(3.68, req.price, 'set correct price')
        self.assertEqual(CFICode.OPTION_PUT.value, req.cfiCode, 'correct cfi code')
        self.assertEqual('5CG05400', req.account, 'set account')
        self.assertEqual('+B.1.a.4', req.text, 'set account') 
        
          
    def test_parse_option_args(self):
        args = 'B BAC 100 20.30 -x 20220929 -s 11.21 -t Put'
        result = api_shell.parse_option_args(args);
        
        values = args.split()
        self.assertEqual(values[5], result.expire_date)
        self.assertEqual(float(values[7]), result.strike_price)
        self.assertEqual(values[9], result.option_type)
                
    
    def test_parse_option_args_missing_symbol_no_exut(self):
        
        args = 'B 100 20.30 -x 20220929 -s 11.21 -t Put'
        result = api_shell.parse_option_args(args);
        self.assertIsNone(result, 'error parsing is caught')
    

    def test_parse_option_args_long_names(self):
        args = 'B BAC 100 20.30 --expire-date 20220929 --strike-price 11.21 --option-type Put'
        result = api_shell.parse_option_args(args);
        
        values = args.split()
        self.assertEqual(values[5], result.expire_date)
        self.assertEqual(float(values[7]), result.strike_price)
        self.assertEqual(values[9], result.option_type)

    def test_send_new_option_order(self):
        args = 'B BAC 100 20.30 -x 20220929 -s 11.21 -t Put'
        self.shell.do_option(args)
        self.assertEqual(1, len(self.client), "sent order")
        req = self.client.first()
        self.assertEqual(100, req.orderQty, 'set correct qty')
        self.assertEqual(20.30, req.price, 'set correct price')
        self.assertEqual('202209', req.maturityMonthYear)
        self.assertEqual(29, req.maturityDay)
        self.assertEqual(11.21, req.strikePx)
        self.assertEqual(CFICode.OPTION_PUT.value, req.cfiCode)
        
    def test_option_missing_required_fields(self):
        args = 'B BAC 100 20.30 -x 20220929 -t Put' #missing strikepx
        with self.assertRaises(ValueError) as context:
            self.shell.do_option(args)
        
        thrown =  context.exception
        print(thrown)
        self.assertTrue('strike_price' in str(thrown))

    def test_bad_expire_date(self):
        args = 'B BAC 100 20.30 -x 202209 -t Put --strike-price 1.11' 
        with self.assertRaises(ValueError) as context:
            self.shell.do_option(args)
        
        thrown =  context.exception
        print(thrown)
        # self.assertTrue('strike_price' in str(thrown))
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_send_new']
    unittest.main()
