[![PyPI version](https://img.shields.io/pypi/v/ezx-pyapi)](https://pypi.org/project/ezx-pyapi/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ezx-pyapi)
[![GitHub last commit](https://img.shields.io/github/last-commit/EZXInc/ezx-sample-py)](https://github.com/EZXInc/ezx-sample-py)

# 📦 ezx-sample-py

Sample Application to demonstrate how to use the EZX iServer API. This is a limited example showing how the EZX Python API is used to send orders and process the responses from the iServer and the Exchanges.

📘 **For detailed documentation of API messages, including advanced usage and full message structure, see the [EZX Sample App Wiki](https://github.com/EZXInc/ezx-sample-py/wiki).**

---

## 🧰 Requirements

- Python **3.8 or higher**

---

## 📥 Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/EZXInc/ezx-sample-py.git
    ```

2. Install the EZX iServer API from PyPI:

    ```bash
    pip install ezx-pyapi
    ```

---

## ▶️ Running the Sample Application

Contact [EZX](http://www.ezxinc.com/) to set up a demo account. This will give you a **company**, **user**, and **password** to log into the server.

> **Note:** Python files are in the `src` directory. You can either navigate to that folder or set your `PYTHONPATH` to include it.

Run the app:

```bash
python ezx_sample.py -s <your server> -p <port> -c <your company> -u <user> -pw <password>
```

Once connected, you'll see a command-line prompt. If not, press `<Enter>` to wake it up.

To see available commands:

```bash
help
```

For help with a specific command:

```bash
help <command>
```

---

## 📝 Logging

Logging is controlled by the `logging.ini` file. By default, debug messages are printed to the console.

---

## 🧠 Understanding the Sample Code

The sample functions for interacting with the iServer API are located in:

```
api_functions.py
```

---

## 🧪 Interactive Mode

You can use the API interactively by importing from `interactive.py`.

```python
from interactive import *

# connect(company, user, password, host, [optional:port]
client = connect('ABCCOMPANY', 'test1', 'test1', 'eval.ezxinc.com')

# Send an order
from iserver.msgs.convenience_msgs import *
from iserver.enums.msgenums import Side

order = NewOrder('ZVZZT', Side.BUY.value, 100, 1.25, 'SIMU')
client.send_message(order)
```

### Available functions

Type `show_help()` in the interactive session to view available functions:

```text
connect      - Connect to the iserver.
stop         - Disconnect from the iserver.
status       - Check if the client is logged in.
show_help    - Display interactive commands.
```

Example commands:

```python
status()
client.send_message(ReplaceOrder(551, -1.24, 60))
client.send_message(CancelOrder(551))
stop()
```

### Custom Response Handler

You can override the default handler like so:

```python
from iserver.msgs.OrderResponse import OrderResponse
import iserver.net

responses = []

def my_msg_handler(msg_subtype: int, msg: EzxMsg):
    iserver.net.empty_msg_handler(msg_subtype, msg)  # prints it
    responses.append(msg)

client._msg_handler = my_msg_handler
client.send_message(order)
```

📘 Also see the [EZX API Quick Start Guide](https://docs.google.com/document/d/1VcAYjFDZfIbQCVmVN4CZ_U6d3O3dHbnFNuiIBec8L3M).

---

## 🧾 Exotic Order Types

### 🧱 MultiLeg Orders

Multileg orders are created by building a parent `OrderRequest` and adding legs.

```python
from orders import *
from iserver.enums.msgenums import Side, CFICode

mleg = MultilegOrder(price, qty, destination, account)
mleg.add_leg(EquityLegOrder(symbol, Side.BUY, shares_ratio))
mleg.add_leg(OptionLegOrder(symbol, Side.SELL, contracts_ratio, CFICode.OPTION_CALL, strikePx, '20231215'))

client.send_message(mleg)
```

#### Responses

Each Multileg order produces:

- A parent `OrderResponse`
- One response per leg (with `refID`)
- All responses share the same `basketID`

#### Replaces

```python
client.send_message(ReplaceOrder(orderID, price, qty))
```

#### Cancels

```python
client.send_message(CancelOrder(orderID))
```

---

### 🧾 SecurityDefinition Requests (CME)

SecurityDefinition requests allow you to request strategy instruments (like spreads or combos) from CME.

```python
from interactive import *
from iserver.msgs.SecurityLegInfo import SecurityLegInfo
from iserver.msgs.convenience_msgs import ComboSecurityDefinitionRequest

req = ComboSecurityDefinitionRequest(
    account="SIMU",
    destination="CME_AUTOCERT",  # replace with your configured destination
    legs=[
        SecurityLegInfo(securityID="654321", side=2, ratioQty=1),
        SecurityLegInfo(securityID="123456", side=1, ratioQty=1),
    ]
)

client.send_message(req)
```

📘 For a complete guide to required fields and responses, see:  
📄 [SecurityDefinitionRequest API Notes (CME)](https://github.com/EZXInc/ezx-sample-py/wiki/SecurityDefinitionRequest)

---
