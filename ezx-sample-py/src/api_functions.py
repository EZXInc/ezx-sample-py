'''
Created on 10 Mar 2022

@author: shalomshachne
'''
import threading

from iserver import util
from iserver.enums import api
from iserver.enums.api import IserverMsgSubType
from iserver.enums.msgenums import MsgType, Side, OrdType, CFICode
from iserver.msgs.OrderRequest import OrderRequest
from iserver.net import ApiClient, ConnectionInfo, ClientState
from iserver.msgs.OrderResponse import OrderResponse
from iserver.msgs.Reject import Reject
import iserver
from iserver.msgs.convenience_msgs import CancelOrder, NewOrder, ReplaceOrder

destination = 'SIMU'
client: ApiClient = None

sides = {'B': Side.BUY, 'S': Side.SELL, 'SS': Side.SELL_SHORT}

pending_orders = {}  # cache by myID to link back to first response to a new order 

open_orders = {}  # cache by routerOrderID to find orders by id.

wait_for_connection = threading.Condition()


def process_order_update(msg: OrderResponse):
    # do stuff like update position
    try:
        if util.is_closed(msg):
            order = open_orders.pop(msg.routerOrderID)
            print(f'removed closed order={order}')
        else:
            open_orders[msg.routerOrderID] = msg
            
    except Exception as e:
        print(f'error processing OrderResponse. ex={e}')
        

def process_reject(msg: Reject):
    pass  # deal with having a NEW, REPL or CANC rejected.


def get_open_orders():
    '''
    returns an iterator of the open orders.
    '''
    return iter(open_orders.values())

def get_pending_order(myID : str) -> OrderRequest:
    return pending_orders.get(myID)


def msg_handler(msg_subtype, msg):
    print(f'\nreceived server response={msg}')
    try:
        if msg.myID in pending_orders:
            pending_orders.pop(msg.myID)
    except AttributeError:
        pass
    
    if api.IserverMsgSubType.ORDERRESPONSE.value == msg_subtype:
        process_order_update(msg)
    elif api.IserverMsgSubType.REJECT.value == msg_subtype:
        process_reject(msg)
    else:
        pass  # all we care about now
    
    
def on_state_change(state: ClientState):
    print(f'client state={state}')
    if state == ClientState.LOGGED_IN:
        with wait_for_connection:            
            wait_for_connection.notify_all()


   

def send_new_order(side, symbol, qty, price, **kwargs):
    qty = int(qty)
    price = float(price)
    side = parse_side(side)
    
    order = NewOrder(symbol, side, qty, price, destination, util.next_id())
    # set additional properties of the order
    if kwargs:
        iserver.set_properties(order, kwargs)
        
    pending_orders[order.myID] = order
    client.send_message(order)
    
def send_new_option(side, symbol, qty, price, expire_date, option_type, strike_price):
    qty = int(qty)
    price = float(price)
    side = parse_side(side)
    
    order = NewOrder(symbol, side, qty, price, destination, util.next_id())
    year_month, day = parse_expire_date(expire_date)
    order.maturityMonthYear = year_month
    order.maturityDay = day
    order.cfiCode = parse_option_type(option_type)
    order.strikePx = strike_price
    
    client.send_message(order)
        
    
def cancel(routerOrderID : int):
    client.send_message(CancelOrder(routerOrderID))    
    
def replace_order(routerOrderID, price, qty = None):
    roid = int(routerOrderID)
    if not roid in open_orders:
        print(f'error: no order found for roid={roid}')
        return
    
    price = float(price)
    if qty:
        qty = int(qty)
    client.send_message(ReplaceOrder(roid, price, qty))
    
    

def parse_side(sideName: str) -> int:
    try:
        return sides[sideName].value
    
    except KeyError:
        raise ValueError(f'invalid side specified! allowed=B, S, SS, was {sideName}')

def parse_expire_date(expire_date):
    if len(expire_date) < 8:
        raise ValueError(f'expire_date format=YYYYMMDD, value was=[{expire_date}]')    
    return expire_date[0:6], int(expire_date[-2:])
    
def parse_option_type(option_type):    
    if option_type.casefold() == 'Put'.casefold():
        return CFICode.OPTION_PUT.value
    if option_type.casefold() == 'Call'.casefold():
        return CFICode.OPTION_CALL.value
    
    raise Exception(f'invalid option type [{option_type}]')
    
    
def stop_client():
    ''' 
    shut down client 
    '''
    if client: client.stop()

    
def start_client(connection_info: ConnectionInfo): 
    global client
    client = ApiClient(connection_info, msg_handler, on_state_change)    
    with wait_for_connection:
        print('starting ApiClient and waiting 10 seconds for connection...')
        client.start()
        wait_for_connection.wait(30)
    if not client.is_loggedin():
        raise BaseException(f'unable to login to {connection_info}')    
    print('logged in, you can start sending orders')    
