[![PyPI version](https://badge.fury.io/py/ezx-pyapi.svg)](https://badge.fury.io/py/ezx-pyapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ezx-pyapi)
[![GitHub last commit](https://img.shields.io/github/last-commit/EZXInc/ezx-sample-py)](https://github.com/EZXInc/ezx-sample-py)

# ezx-sample-py

Sample Application to demonstrate how to use the EZX iServer API. This is a limited example showing how the EZX Python API is used to send orders and process the responses from the iServer and the Exchanges.


# Dependencies and Installation

Install the EZX iServer API (ezx-pyapi).

```python
pip install ezx-pyapi
```

Then clone this repository to get the sample app.


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

The sample functions for interacting with the iServer API are in the api_functions.py module.  



# EZX API Notes


The iServer API is not really designed to be run interactively, although it is possible to do it, as shown below. 


```python

	import logging
	import sys
	FORMAT='%(asctime)s %(levelname)s: Thread-%(thread)d %(name)s %(funcName)s  %(message)s'
	logging.basicConfig(level=logging.INFO,format=FORMAT,stream=sys.stdout,force=True)
	from iserver.net import ConnectionInfo,ApiClient
	info = ConnectionInfo(host='192.168.1.218',company='FEIS',user='igor',password='igor', port=15000)
	client=ApiClient(info)
	client.start()
	
	# send an order
	from iserver.msgs.convenience_msgs import NewOrder
	order = NewOrder('ZVZZT',1,100,1.25,'SIMU')
	client.send_message(order)
	
```

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

