# bittrex-py
A simple Python module for the Bittrex Exchange API (v1.1).

## Usage
Download bittrex.py and place it either with the script you intend to use it with, or in the Python Lib directory.  

API keys can be created here: https://bittrex.com/Manage#sectionApi  

The module can be used by importing the module then creating a Bittrex object.
```python
from bittrex import Bittrex

b = Bittrex('api key', 'secret')
```
    
The arguments can be left blank if you only wish to use public API methods.
```python
from bittrex import Bittrex

b = Bittrex()
```

# Methods

## Public API methods (no API key or secret needed)

**.markets()**  
Used to get the open and available trading markets at Bittrex along with other meta data.  
*Parameters:*  
None

**.currencies()**  
Used to get all supported currencies at Bittrex along with other meta data.  
*Parameters:*  
None

**.ticker('market')**  
Used to get the current tick values for a market.  
*Parameters:*  

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth').

**.marketsummaries()**  
Used to get the last 24 hour summary of all active markets.  
*Parameters:*  
None

**.marketsummary('market')**  
Used to get the last 24 hour summary for a given market.  
*Parameters:*  

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth').

**.orderbook('market', 'type', 'depth')**  
Used to get the orderbook for a given market.  
*Parameters:*  

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth').  
type | required | Buy, sell or both to identify the type of orderbook to return.  
depth | optional | Defaults to 20. How deep of an order book to retrieve. Max is 50

**.markethistory('market')**  
Used to get the latest trades that have occured for a specific market.  
*Parameters:*  

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth').

## Market API methods (API key and secret are needed)
Make sure you have the proper permissions set on your API keys for these to work. 

**.buylimit('market', 'quantity', 'rate')**  
Used to place a buy order in a specific market.  
*Parameters:*

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth').  
quantity | required | The amount to purchase.
rate | required | The rate at which to place the order.

**.selllimit('market', 'quantity', 'rate')**  
Used to place a sell order in a specific market.  
*Parameters:*

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth').  
quantity | required | The amount to purchase.
rate | required | The rate at which to place the order.

**.cancel('uuid')**  
Used to cancel a buy or sell order.  
*Parameters:*

parameter|required|description
---|---|:---
uuid | required | Uuid of the buy or sell order.  

**.openorders('market')**  
Get all orders that you currently have opened. A specific market can be requested.  
*Parameters:*

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth').

## Account API methods (API key and secret are needed)
Make sure you have the proper permissions set on your API keys for these to work. 

**.balances()**  
Used to retrieve all balances from your account.  
*Parameters:*  
None

**.balance('currency')**  
Used to retrieve the balance from your account for a specific currency.
*Parameters:*

parameter|required|description
---|---|:---
currency | required | A string literal for the currency (eg: 'btc').

**.depositaddress('currency')**  
Used to retrieve or generate an address for a specific currency. If one does not exist, the call will fail and return ADDRESS_GENERATING until one is available.  
*Parameters:*

parameter|required|description
---|---|:---
currency | required | A string literal for the currency (eg: 'btc').

**.withdraw('currency', 'quantity', 'address', 'paymentid')**  
Used to withdraw funds from your account. *note: please account for transaction fee.*  
*Parameters:*  

parameter|required|description
---|---|:---
currency | required | A string literal for the currency (eg: 'btc').
quantity | required | The quantity of coins to withdraw.
address | required | The address where to send the funds.
paymentid | optional | Used for CryptoNotes/BitShareX/Nxt optional field (memo/paymentid).

**.getorder('uuid')**  
Used to retrieve a single order by uuid.  
*Parameters:*

parameter|required|description
---|---|:---
uuid | required | Uuid of the buy or sell order.  

**.orderhistory('market')**  
Used to retrieve your order history. A specific market can be requested.  
*Parameters:*

parameter|required|description
---|---|:---
market | required | A string literal for the market (eg: 'btc-eth'). If ommited, will return for all markets.

**.withdrawalhistory('currency')**  
Used to retrieve your withdrawal history. A specific currency can be requested.  
*Parameters:*

parameter|required|description
---|---|:---
currency | required | A string literal for the currency (eg: 'btc'). If ommited, will return for all currencies.

**.deposithistory('currency')**  
Used to retrieve your deposit history. A specific currency can be requested.  
*Parameters:*

parameter|required|description
---|---|:---
currency | required | A string literal for the currency (eg: 'btc'). If ommited, will return for all currencies.