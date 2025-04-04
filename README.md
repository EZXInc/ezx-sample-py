[![PyPI version](https://badge.fury.io/py/ezx-pyapi.svg)](https://badge.fury.io/py/ezx-pyapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ezx-pyapi)
[![GitHub last commit](https://img.shields.io/github/last-commit/EZXInc/ezx-sample-py)](https://github.com/EZXInc/ezx-sample-py)

# ezx-sample-py

Sample Application to demonstrate how to use the EZX iServer API. This is a limited example showing how the EZX Python API is used to send orders and process the responses from the iServer and the Exchanges.

Requires Python 3.8 or higher.

Dependencies and Installation

1. Clone this repository

2. Install the EZX iServer API (ezx-pyapi):
```python
pip install ezx-pyapi
```


# Running the Sample Application

Contact [EZX](http://www.ezxinc.com/) to set up a demo account. This will give you a company, user and password to log into the server.  **Note:** The python files are in the *src* directory, so either navigate to the folder, or set your *PYTHONPATH* to include the *src* directory.

To run the app (after installing dependencies): 


```bash
python ezx_sample.py -s <your server> -p <port> -c <your company> -u <user> -pw <password>  
```

This will give you a command line interface which allows you to send new orders and to replace/cancel them.  If you don't see the command prompt (*$*) press &lt;Enter&gt;. (By default, the app is logging DEBUG messages to the console.  These can be turned off, see below.)

To see the available commands, type:

```bash
	help
```
For help with a specific command, type:

```bash
	help <command>
```

## Logging

Logging is controlled by the *logging.ini* file. 




# Understanding the Sample Code

The sample functions for interacting with the iServer API are in the `api_functions.py` module.  



# EZX API Notes


The iServer API is not really designed to be run interactively, although it is possible to do it, as shown below. 


```python

	from interactive import * #this creates an interactive connection to the iserver
	
	
	# send an order
	from iserver.msgs.convenience_msgs import *
	order = NewOrder('ZVZZT',1,100,1.25,'SIMU')
	client.send_message(order)
	
	# type: show_help() to display available functions in the interactive environment
	
	Available functions: (type help(function name) to see the parameters for the function.):
	----------------------------------------------------------------------------------------
	connect - Connect to the iserver.
	stop - Disconnect from the iserver.  You will need to call the connect method again to reconnect.
	status - Indicates connection status. if connected=True, then the client is logged in to the iserver.
	show_help - Displays information about available functions.
	----------------------------------------------------------------------------------------
	
	 status()
	 iserver client connected=True. company=EROOM, user=test1
	 
	 # Replace an order
	 client.send_message(ReplaceOrder(551, -1.24, 60))
	 
	 # Cancel an order
	 client.send_message(CancelOrder(551))
	 
	 # disconnect
	 stop()
	 
	
```

**More...**
The default message handler just prints the responses from the server.  You can set your own handler as follows:

```python

	from iserver.msgs.OrderResponse import OrderResponse
	
	responses = []
	import iserver.net
	def my_msg_handler(msg_subtype: int, msg: EzxMsg):
		iserver.net.empty_msg_handler(msg_subtype, msg) # print the message
		# write your handling logic here.
		responses.append(msg)
		
	client._msg_handler = my_msg_handler  # normally this is set in the ApiClient constructor
	
	client.send_message(order)
			
```

Also see the [EZX API Quick Start Guide](https://docs.google.com/document/d/1VcAYjFDZfIbQCVmVN4CZ_U6d3O3dHbnFNuiIBec8L3M) for more details on the API.

# Exotic Order Types
## MultiLeg Orders
Sending MultiLeg orders is virtually the same as sending individual orders.  You create a "parent" OrderRequest object and then add to the OrderRequest.legList additional OrderRequest objects for each leg.

On Multileg orders, price and quantity are set on the "parent" only. On each leg, you specify side, symbol, and ratio (multiplier for the parent quantity).  For Option legs, additionally specify the standard option parameters.

There are some helper classes located in the `orders` module for creating MultiLeg orders.  Sample code below.

```python
from orders import *
from iserver.enums.msgenums import Side,CFICode,MsgType

...

mleg = MultilegOrder(price, qty, destination, account)
mleg.add_leg(EquityLegOrder(symbol, Side.BUY, shares_ratio)
mleg.add_leg(OptionLegOrder(symbol, Side.SELL, contracts_ratio, CFICode.OPTION_CALL, strikePx, '20231215')

client.send_message(mleg)

```

### Responses from the API
Although the Multileg order is sent as a single message, the iServer responds with separate OrderResponse messages for the parent and each leg. So for a 2-leg MultiLeg order, there will be 3 OrderResponses returned by the iServer. The iServer also calculates the *orderQty* for the leg OrderResponses (`ratioQty * parent.orderQty`).

OrderResponse messages for MultiLeg orders will have a *basketID* field which will contain the same value for all the orders belonging to the Multileg. This is useful for linking the separate responses to the MultiLeg order. OrderResponse messages for the leg orders will additionally have *refID* field set with a unique value (on this order) for each leg.

### Replaces
Replaces follow the same pattern as replacing a regular order.  In general, only values on the *parent* order can be replaced (usually only price and orderQty). You only need to set the *routerOrderID*, *price* and/or *orderQty* on the replace request.  For example:

```python
	client.send_message(ReplaceOrder(orderID, price, qty)		
```

### Cancels
This is the same as canceling a standard order. Use the *CancelOrder* message as shown in the sample app.

## SecurityDefinition Messages (CME)
Users can send SecurityDefintionRequest messages to CME using the API. The message flow is much simpler than standard orders.  A request is sent and will either be accepted, or rejected.  If accepted, use the *securityID* value sent back on the response from the exchange.

A sample interactive session which sends the requests and receives the responses is below.







