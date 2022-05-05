'''
Created on 11 Mar 2022

@author: shalomshachne
'''
import inspect
import random
import string

from iserver.enums.msgenums import LogonType
from iserver.net import ConnectionInfo


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
  