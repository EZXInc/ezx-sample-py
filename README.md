[![PyPI version](https://badge.fury.io/py/ezx-pyapi.svg)](https://badge.fury.io/py/ezx-pyapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ezx-pyapi)
[![GitHub last commit](https://img.shields.io/github/last-commit/EZXInc/ezx-sample-py)](https://github.com/EZXInc/ezx-sample-py)

# ezx-sample-py
EZX iServer API for Python - Sample Application to demonstrate how to use the EZX iServer API


## Dependencies and Installation
Install ezx-pyapi to connect with the iServer.

```python
pip install ezx-pyapi
```

Then clone or fork this [repository](https://github.com/EZXInc/ezx-sample-py.git).

## Running the Sample Application
Contact [EZX](http://www.ezxinc.com/) to set up a demo account. This will give you a company, user and password to log into the server.

To run the app (after installing dependencies):

```bash
python ezx_sample.py -s <your server> -p <port> -c <your company> -u <user> -pw <password>  
```

This will give you a command line interface which allows you to send new orders and to replace/cancel them.


