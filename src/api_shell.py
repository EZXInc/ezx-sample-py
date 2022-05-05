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
import argparse
from argparse import Namespace, ArgumentParser


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
    
    def do_option(self, args):

        properties = {}
        parsed = parse_option_args(args)
        if parsed.properties:
            properties = iserver.parse_to_dict(parsed.properties)

        if parsed:
            api_functions.send_new_option(parsed.side, parsed.symbol, parsed.qty, parsed.price, parsed.expire_date, parsed.option_type, parsed.strike_price, **properties)
        
    def help_option(self):
        print('\nsend a new Option order to the iserver.')
        print('usage: option Side Symbol Qty Price -x Expiration -s StrikePrice -t Option Type [-p optional1=value1, optional2=value2]')
        print('example: option S TSLA 10 5.20 -x 20220918 -s 899 -t Put -p account=MYACC,senderSubID=trader')
        print('\n')
        print('required Option arguments:')
        print('-x --expire-date Expiration Date (YYYYMMDD)')
        print('-s --strike-price Strike Price')
        print('-t --option-type Option Type (Put or Call)')
        print('\noptional order values:')
        print('-p --properties name1=value1,name2=value2 (comma separated list of name/value pairs')
        
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
        
    
def create_options_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(prog='option')
    
    option_values = parser.add_argument_group('option values')
    option_values.add_argument('-x', '--expire-date', type=str, help='expiration date in format YYYYMMDD', dest='expire_date')
    option_values.add_argument('-s', '--strike-price', type=float, help='strike price', dest='strike_price')
    option_values.add_argument('-t', '--option-type', type=str, help='option type (Put or Call)', dest='option_type')
    
    order_values = parser.add_argument_group('order values')
    order_values.add_argument('side', type=str)
    order_values.add_argument('symbol', type=str)
    order_values.add_argument('qty', type=int)
    order_values.add_argument('price', type=float)    
    order_values.add_argument('-p', '--properties', type=str, help="optional order properties to set", dest='properties')
    
    # parser.exit = exit_override
    def error_override2(message):
        # parser.print_usage(sys.stderr)
        raise argparse.ArgumentError(None, message)
    
    parser.error = error_override2
    
    return parser
    
    
def parse(args: str) -> list:
    return tuple(args.split())


def parse_option_args(args: str) -> Namespace:
    option_parser = create_options_parser()    
    args = parse(args)
    try:
        result = option_parser.parse_args(args)
        validate_option_values(option_parser, result)
        return result
    except argparse.ArgumentError as e:
        print(f'error: {e.message} \n', file=sys.stderr)
        option_parser.print_help()


def validate_option_values(parser: ArgumentParser, values: Namespace): 
    ''' Check that there are valid values for all option fields, throws Exception otherwise '''
    for action in parser._actions:
        if not action.type or action.dest == 'properties':
            continue
        
        dest = action.dest
        try:
            value = getattr(values, dest)
            if not value:
                raise ValueError(f'missing required value for {dest}')   
        except:
            raise ValueError(f'missing required value for {dest}')


def start(connection: ConnectionInfo):
    api_functions.start_client(connection)
    shell = ApiCommands()
    shell.cmdloop("enter a command (or help)")

