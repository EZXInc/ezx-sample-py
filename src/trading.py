'''
Created on 12 Sep 2022

@author: shalomshachne
'''
from iserver.msgs.ExecutionStatus import ExecutionStatus
from iserver.enums.msgenums import Events, Side

def sign(value : float):
    return 1 if value > 0 else 0 if value == 0 else -1

class Position(object):
    
    def __init__(self, symbol : str = None, shares : int = 0, avg_price : float = 0.0):
        self.symbol : str = symbol
        self.shares : int = shares
        self.buy_avg: float = 0.0
        self.sell_avg: float = 0.0
        self.sold_shares: int= 0
        self.bought_shares: int = 0
        if shares > 0:
            self.bought_shares = shares
            self.buy_avg = avg_price
        elif shares < 0:
            self.sold_shares = shares
            self.sell_avg = avg_price
            
    
    def update(self, api_side : int, execution : ExecutionStatus):
        if not Events.EXEC.value == execution.event:
            return 
        
        multiplier = 1 if api_side == Side.BUY.value else -1
        if multiplier != sign(self.shares):
            #closing position
            pass
        
        filled = int(execution.lastShares) # force value to be int not float.
        price = execution.lastPrice                        
        self.shares += filled * multiplier
        
        if multiplier == 1:  # buy
            self.update_avg(self.bought_shares, self.buy_avg, filled, price, self.set_buy_avg)
            self.bought_shares += filled
        else:
            self.update_avg(self.sold_shares, self.sell_avg, filled, price, self.set_sell_avg)
            self.sold_shares += filled
                       
    
    def set_buy_avg(self, new_price: float):
        self.buy_avg = new_price
        
    def set_sell_avg(self, new_price: float):
        self.sell_avg = new_price
       
    def update_avg(self, previous_shares, previous_avg, new_shares, new_price, setter):
        new_avg = (previous_shares * previous_avg + new_shares * new_price) / (previous_shares + new_shares)
        setter(new_avg)
        
    def __str__(self, *args, **kwargs):
        return f'{self.symbol}: shares={self.shares:,d}, buy history(shares={self.bought_shares:,d}, avg price={self.buy_avg:.2f}), sell history=(shares={self.sold_shares:,d}, avg price={self.sell_avg:.2f})'
    