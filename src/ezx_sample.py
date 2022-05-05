'''
Created on 8 Mar 2022

@author: shalomshachne
'''
import argparse

import api_shell
from iserver.net import ConnectionInfo
import os
import logging.config
import sys


my_path = os.path.dirname(os.path.abspath(__file__))
log_config=f'{my_path}/logging.ini'
if not os.path.exists(log_config):
    print(f'error: cannot find logging config at {log_config}')
    sys.exit(1)

logging.config.fileConfig(log_config)



if __name__ == "__main__":
    parser = argparse.ArgumentParser("ezx_sample ")
    parser.add_argument('-s',help='server address', type=str, dest='host', required=True)
    parser.add_argument('-p',help='port', type=int, dest='port', required=True)
    parser.add_argument('-c', help='company', type=str, dest='company', required=True)
    parser.add_argument('-u',help='user', type=str, dest='user', required=True)
    parser.add_argument('-pw',help='password', type=str, dest='password', required=True)
    args = parser.parse_args()
    print(args)
        
    info = ConnectionInfo(**vars(args))
    print(f'info={info}')
    
    api_shell.start(info)
    
    
    
    