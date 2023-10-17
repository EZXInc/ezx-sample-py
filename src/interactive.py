import logging
import sys
import json

FORMAT = '%(asctime)s %(levelname)s: Thread-%(thread)d %(name)s %(funcName)s  %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stdout, force=True)

from iserver.net import ConnectionInfo, ApiClient
# make it easy to access these objects by importing here.
from iserver.msgs.convenience_msgs import *
from iserver.enums.msgenums import LogonType

client = None
info = None

def create_connection_info(company, user, password, host, port=15000):
    return ConnectionInfo(host=host, company=company, user=user, password=password, port=port, logon_type=LogonType.SENDONLY.value)


def connect(company, user, password, host, port=15000):
    """Connect to the iserver.
    
        Args:
            company (str): iServer company name
            user (str): user login id
            password (str): 
            host (str)
            port (int) (defaults to 15000)
    
        Returns:
            an ApiClient instance. This is also accessible referencing the badge.client object
    """    
    global info
    info = create_connection_info(company, user, password, host, port)
    global client
    client = ApiClient(info)
    client.start()
    print('iserver client started...')
    return client

    
def stop():
    """Disconnect from the iserver.  You will need to call the connect method again to reconnect.
    """
    global client
    if client:
        client.stop()        
        client = None
        print('disconnected.')
    else:
        print('not connected')   

def status(): 
    """Indicates connection status. if connected=True, then the client is logged in to the iserver.
    """
    global client
    if client:
        print(f'iserver client connected={client.is_loggedin()}. company={info.company}, user={info.user}')
    else:
        print('not connected to iserver.')

def show_help():
    """Displays information about available functions."""
    print("Available functions: (type help(function name) to see the parameters for the function.):")
    print("----------------------------------------------------------------------------------------")
    for name, func in globals().items():
        if callable(func) and func.__doc__:
            doc = func.__doc__.split('\n')[0]
            if doc:
                print(f"{name} - {doc}")

    print("----------------------------------------------------------------------------------------\n\n")
    
    
print('\n\n\nThis creates an iteractive connection to the iServer, and allows you to interactively send orders.\n\n')
show_help()

