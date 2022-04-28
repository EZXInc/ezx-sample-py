'''
Created on 8 Mar 2022

@author: shalomshachne
'''
from cmd import Cmd
import sys

import api_functions
from iserver import util
import iserver
from iserver.net import ConnectionInfo


class ApiCommands(Cmd):
    prompt = "$ "
    
    def do_new(self, args):
        print(f'sending new order with {args}')  
        args = parse(args)
        properties = {}
        if len(args) > 4:
            properties = iserver.parse_to_dict(','.join(args[4:]), ',')
            args = args[0:4]
        api_functions.send_new_order(*args, **properties)
       
        
    def help_new(self):
        print('send a new order to the iserver. Required arguments are Side, Symbol, Qty. If price is empty, it will be a market order.')
        print('additional order properties can be set by entering a comma separated list of name=value pairs.')
        print('syntax: new <side=B or S> <symbol> <qty> <price> [optional1=value1, optional2=value2]')
        print('example: S TSLA 1000 989.20 account=1,text=+B.1.a.4')
        
        
    def do_cancel(self, args):
        'Cancel an order:  cancel <roid>'
        print(f'canceling order {args}')
        api_functions.cancel(int(args))
        
        
    def do_replace(self, args):
        args = parse(args)
        api_functions.replace_order(*args)
    
    def help_replace(self):
        print('replace open order with new price and/or qty')
        print('syntax: replace <roid> price [qty]')
        print('example: replace 201 25.26')
        print('(use the "list orders" command to see the routerOrderIDs (roid) of the open orders)')
        
        
        
    def do_list(self, args):
        'list [orders]'
        if ('orders' in args):
            print('open orders:')
            for order in api_functions.get_open_orders():
    
                print(iserver.util.format_order(order))
                                      
    
    def do_exit(self, inp):
        print('disconnecting from iserver')
        api_functions.stop_client()
        print("Bye")
        return True
    
    
    def default(self, inp):
        print(f'unknown command {inp}')
        
    def onecmd(self, line):
        try:
            return Cmd.onecmd(self, line)
        except Exception as e:
            print(f'error: {e}', file=sys.stderr)
            return False
        
    def emptyline(self):
        pass
        
    do_EOF = do_exit
    
    do_quit = do_exit
    
    do_x = do_exit
    
def parse(args):
    return tuple(args.split())

def start(connection : ConnectionInfo):
    api_functions.start_client(connection)
    shell = ApiCommands()
    shell.cmdloop("enter a command (or help)")
    

