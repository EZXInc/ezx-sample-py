'''
Created on 11 Oct 2023

@author: shalomshachne
'''
from iserver.msgs.OrderRequest import OrderRequest
from iserver.enums.msgenums import Side, CFICode, SecType, MsgType



class MultiLegOrder(OrderRequest):

    def __init__(self, price: float, quantity:float, destination=None, account=None):
        '''
         Construct new MultiLegOrder order. 
         
         Args:
             price (float): price can be any value, including negative numbers
             quantity (float): Buy or Sell
             destination (str): where to route the order
             account (str)
         '''        
        
        super().__init__()
        self.msgType = MsgType.NEW.value
        self.price = price
        self.orderQty = quantity
        self.destination = destination        
        self.account = account
        self.securityType = 'MLEG'
        self.symbol = 'NA'
        side = Side.BUY if price >= 0 else Side.SELL
        self.side = side.value
        
        self.legList = []
        
    def add_leg(self, leg: OrderRequest):
        self.legList.append(leg)
        
    def get_leg(self, index: int):
        return self.legList[index]
        
        
class EquityLegOrder(OrderRequest):

    def __init__(self, symbol: str, side: Side, ratioQty):
        '''
         Construct new Option leg order. 
         
         Args:
             symbol (str): root symbol
             side (Side enum): Buy or Sell
             ratioQty multiplier to apply to the orderQty specified in the parent order.
         '''        
        super().__init__()
        self.securityType = SecType.COMMON_STOCK.value
        self.ratioQty = ratioQty
        self.side = side.value
        self.symbol = symbol
       


class OptionLegOrder(OrderRequest):

    def __init__(self, symbol: str, side: Side, ratioQty, cfiCode: CFICode, strikePrice: float, maturityDate: str):
        '''
        Construct new Option leg order. 
        
        Args:
            symbol (str): root symbol
            side (Side enum): Buy or Sell
            ratioQty multiplier to apply to the orderQty specified in the parent order.
            cfiCode (CFICode enum): Put or Call
            strikePrice (float): strike price of the option
            maturityDate (str) ANSI date YYYYMMDD       
        '''
        super().__init__()
        self.securityType = SecType.OPTION.value        
        self.ratioQty = ratioQty
        self.side = side.value
        self.symbol = symbol
        self.cfiCode = cfiCode.value
        self.strikePx = strikePrice
        self.maturityMonthYear = maturityDate[:6]
        self.maturityDay = int(maturityDate[6:])
        
         
