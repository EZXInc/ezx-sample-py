'''
Created on 11 Mar 2022

@author: shalomshachne
'''
import inspect
import random
import string

from iserver.enums.msgenums import LogonType, State, Events
from iserver.net import ConnectionInfo
from iserver.msgs.OrderRequest import OrderRequest
from iserver.msgs.OrderResponse import OrderResponse
from iserver.msgs.ExecutionStatus import ExecutionStatus


__next_int = 0

def create_connection_info(host='localhost', port=15000, user='aUser', password='aPasswd!', company='MyCompany', logon_type=LogonType.ALL.value):
    info = inspect.getargvalues(inspect.currentframe())
    args = info.locals 
    return ConnectionInfo(**args)
    
def next_int_id():
    global __next_int
    __next_int = __next_int + 1
    return __next_int

def random_symbol(max_chars : int =4) -> str:
    return ''.join(random.choices(string.ascii_uppercase, k=max_chars))

def random_price(min_price : float = .01, max_price : float = 999.99) -> float:
    return round(random.uniform(min_price, max_price), 4)

def random_quantity(min_qty : int = 1, max_qty : int = 5000):
    return random.randint(min_qty, max_qty)

def copy_fields(source : object, target: object):
    properties = vars(source).items()
    for name,value in properties:
        try:
            if name == "msg_subtype":
                continue
            
            setattr(target, name, value)
                
        except:
            pass

def create_fill_response(req : OrderRequest, fill_qty : int = None, fill_price : float = None):
    response = OrderResponse(routerOrderID = next_int_id())
    copy_fields(req, response)
    fill_qty = fill_qty or response.orderQty
    fill_price = fill_price or response.price
    response.state = State.FILLED.value if fill_qty == response.orderQty else State.PAFI.value
    response.event = Events.EXEC.value
    response.cumQty = fill_qty
    response.leavesQty = max(0, response.orderQty - response.cumQty)
    
    status = ExecutionStatus(lastShares = fill_qty, lastPrice = fill_price, event = response.event)
    response.executions = [status]

    return response

    
    
    