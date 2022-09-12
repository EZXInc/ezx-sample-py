[![PyPI version](https://badge.fury.io/py/ezx-pyapi.svg)](https://badge.fury.io/py/ezx-pyapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ezx-pyapi)
[![GitHub last commit](https://img.shields.io/github/last-commit/EZXInc/ezx-sample-py)](https://github.com/EZXInc/ezx-sample-py)

ezx-sample-py
=============
Sample Application to demonstrate how to use the EZX iServer API. This is a limited example showing how the EZX Python API is used to send orders and process the responses from the iServer and the Exchanges.


Dependencies and Installation
=============================
Install the EZX iServer API (ezx-pyapi).

```python
pip install ezx-pyapi
```


Running the Sample Application
==============================
Contact [EZX](http://www.ezxinc.com/) to set up a demo account. This will give you a company, user and password to log into the server.

To run the app (after installing dependencies):

```bash
python ezx_sample.py -s <your server> -p <port> -c <your company> -u <user> -pw <password>  
```

This will give you a command line interface which allows you to send new orders and to replace/cancel them.



Understanding the Code
======================
The sample functions for interacting with the iServer API are in the api_functions.py module.  

