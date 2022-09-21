'''
Created on 12 Sep 2022

@author: shalomshachne
'''
import unittest
from trading import Position
from trading import sign
from iserver.enums.msgenums import Side, Events
from iserver.msgs.ExecutionStatus import ExecutionStatus
from tests import test_data_factory


class Test(unittest.TestCase):

    def setUp(self):
        self.position = Position("ABC")

    def tearDown(self):
        pass

    def testBuyExecutionAddsPosition(self):
        shares = 100
        execution = self.createFill(shares)
        side = 1
        self.position.update(side, execution)
        self.assertEqual(shares, self.position.shares, "added shares")
        self.assertIsInstance(self.position.shares, int, 'has expected data type for shares')
        
    def testSellExecutionSubtractsPosition(self):
        shares = 100
        execution = self.createFill(shares)
        side = 5
        self.position.update(side, execution)
        self.assertEqual(-shares, self.position.shares, "subtracted shares")
        
    def testUpdatesSellAveragePrice(self):
        shares = 100
        price = 1.05

        side = Side.SELL_SHORT.value
        
        execution = self.createFill(shares, price)
        self.position.update(side, execution)
        self.assertEqual(price, self.position.sell_avg, "calculated avg Price")
        
        shares2 = 200
        price2 = 1.10
        execution = self.createFill(shares2, price2)
        self.position.update(side, execution)
        
        expected = (shares * price + shares2 * price2 ) / (shares  + shares2) 
        self.assertEqual(expected, self.position.sell_avg, "calculated avg Price")
        self.assertEqual(shares + shares2, self.position.sold_shares)

        
    
    def testResetsAvgPriceAfterFlipPosition(self):
        shares = 100
        price = 1.05

        side = Side.SELL_SHORT.value
        
        execution = self.createFill(shares, price)
        self.position.update(side, execution)
        self.assertEqual(price, self.position.sell_avg, "calculated sell avg Price")
    
        shares2 = 200
        price2 = 1.01
        
        side = Side.BUY.value
        execution = self.createFill(shares2, price2)
        self.position.update(side, execution)        
        self.assertEqual(price2, self.position.buy_avg, "calculated buy avg Price")
        
    def testConstructor(self):
        shares = test_data_factory.random_quantity()
        avg_price = test_data_factory.random_price()
        position = Position("ABC", shares, avg_price)
        
        self.assertEqual(avg_price, position.buy_avg)
        self.assertEqual(shares, position.bought_shares)
        
        shares *= -1
        position = Position("ABC", shares, avg_price)
        self.assertEqual(avg_price, position.sell_avg)
        self.assertEqual(shares, position.sold_shares)
        
    
    def testToString(self):
        shares = test_data_factory.random_quantity()
        avg_price = test_data_factory.random_price()
        symbol = test_data_factory.random_symbol(4)
        position = Position(symbol, shares, avg_price)
        
        value = str(position)
        print(value)
        self.assertIn(symbol, value, 'printed symbol')
        
        shares = 2000
        price = 1.05

        side = Side.SELL
        
        execution = self.createFill(shares, price)
        position.update(side, execution)        
        value = str(position)
        print(value)
        self.assertIn(f'{shares:,d}', value, 'printed comma formatted shares')
        
        
    def test_sign(self):
        self.assertEqual(1, sign(1))
        self.assertEqual(0, sign(0))
        self.assertEqual(-1, sign(-3))
        
        
                    
        
    def createFill(self, shares: int, price: float=1.0):
        ex = ExecutionStatus();
        ex.event = Events.EXEC.value
        ex.lastShares = float(shares) # simulate API sending double values to the client in the lastShares
        ex.lastPrice = price
        return ex
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
