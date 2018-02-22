import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests


class Bittrex(object):
    """Bittrex object for interacting with the Bittrex API.

    API key and secret can be left blank if you only need to use the public calls.

    Attributes:
        api_key (string): Your Bittrex API key.
        secret (string): Your API secret.
    """

    def __init__(self, api_key='', secret=''):
        """ Inits Bittrex with the API key and secret. """
        self.api_key = api_key
        self.secret = secret

    def __run(self, call, call_type, data={}):
        """The main function of the Bittrex object.

        Args:
            call (string): The API endpoint
            call_type (string): Type of call to make. Can be 'public', 'market' or 'account'
            data (dict): A dict containing the query parameters

        Returns:
            If the call was successful the result will be returned.
            Otherwise an error message will be returned.
        """

        if call_type == 'public':
            url = 'https://bittrex.com/api/v1.1/public/'
        elif call_type == 'market':
            url = 'https://bittrex.com/api/v1.1/market/'
        elif call_type == 'account':
            url = 'https://bittrex.com/api/v1.1/account/'
        else:
            return 'Oops'

        url += '{}?{}'.format(call, urlencode(data))
        
        if call_type != 'public':
            url += '&apikey={}'.format(self.api_key)
            url += '&nonce={}'.format(time.time())
            b_secret = bytes(self.secret, 'latin-1')
            b_url = bytes(url, 'latin-1')
            sig = hmac.new(b_secret, b_url, hashlib.sha512).hexdigest()
            header = {'apisign': sig}
            r_get = requests.get(url, headers=header)
        else:
            r_get = requests.get(url)

        r_json = r_get.json()

        if r_json['result']:
            return r_json['result']
        else:
            return r_json['message']

    # Public
    def markets(self):
        """Used to get available markets along with other metadata.

        Returns:
            Example:
            [{
                "MarketCurrency" : "LTC",
                "BaseCurrency" : "BTC",
                "MarketCurrencyLong" : "Litecoin",
                "BaseCurrencyLong" : "Bitcoin",
                "MinTradeSize" : 0.01000000,
                "MarketName" : "BTC-LTC",
                "IsActive" : true,
                "Created" : "2014-02-13T00:00:00"
            },...]
        """
        return self.__run('getmarkets', 'public')

    def currencies(self):
        """Used to get all supported currencies along with other meta data. 

        Returns:
            Example:
            [{
                "Currency" : "BTC",
                "CurrencyLong" : "Bitcoin",
                "MinConfirmation" : 2,
                "TxFee" : 0.00020000,
                "IsActive" : true,
                "CoinType" : "BITCOIN",
                "BaseAddress" : null
            },...]
        """
        return self.__run('getcurrencies', 'public')

    def ticker(self, market):
        """Used to get the current tick value for a market.

        Args:
            market (string): A string for the market (eg: 'BTC-LTC').

        Returns:
            Example:
            {
                "Bid" : 2.05670368,
                "Ask" : 3.35579531,
                "Last" : 3.35579531
            }
        """
        return self.__run('getticker', 'public', {'market': market})

    def marketsummary(self, market=None):
        """Used to get the last 24 hour market summary. A specific market can be requested.

        Args:
            market (string, optional): A string for the market (eg: 'BTC-LTC'). 

        Returns:
            Example:
            [{
                "MarketName" : "BTC-LTC",
                "High" : 0.01350000,
                "Low" : 0.01200000,
                "Volume" : 3833.97619253,
                "Last" : 0.01349998,
                "BaseVolume" : 47.03987026,
                "TimeStamp" : "2014-07-09T07:22:16.72",
                "Bid" : 0.01271001,
                "Ask" : 0.01291100,
                "OpenBuyOrders" : 45,
                "OpenSellOrders" : 45,
                "PrevDay" : 0.01229501,
                "Created" : "2014-02-13T00:00:00",
                "DisplayMarketName" : null
            },...]
        """
        if market is None:
            return self.__run('getmarketsummaries', 'public')
        else:
            return self.__run('getmarketsummary', 'public', {'market': market})

    def orderbook(self, market, type_):
        """Used to get the orderbook for a given market.

        Args:
            market (string): A string for the market (eg: 'BTC-LTC').
            type (string): 'buy', 'sell' or 'both' to identify the type of orderbook to return. 

        Returns:
            Example:
            {
                "buy" : [{
                        "Quantity" : 12.37000000,
                        "Rate" : 0.02525000
                    },...],
                "sell" : [{
                        "Quantity" : 32.55412402,
                        "Rate" : 0.02540000
                    }, {
                        "Quantity" : 60.00000000,
                        "Rate" : 0.02550000
                    }, {
                        "Quantity" : 60.00000000,
                        "Rate" : 0.02575000
                    }, {
                        "Quantity" : 84.00000000,
                        "Rate" : 0.02600000
                    },...]
            }
        """
        return self.__run('getorderbook', 'public', {'market': market, 'type': type_})

    def markethistory(self, market):
        """Used to get the latest trades that have occured for a specific market.

        Args:
            market (string): A string for the market (eg: 'BTC-LTC').

        Returns:
            Example:
            [{
                "Id" : 319435,
                "TimeStamp" : "2014-07-09T03:21:20.08",
                "Quantity" : 0.30802438,
                "Price" : 0.01263400,
                "Total" : 0.00389158,
                "FillType" : "FILL",
                "OrderType" : "BUY"
            }, {
                "Id" : 319433,
                "TimeStamp" : "2014-07-09T03:21:20.08",
                "Quantity" : 0.31820814,
                "Price" : 0.01262800,
                "Total" : 0.00401833,
                "FillType" : "PARTIAL_FILL",
                "OrderType" : "BUY"
            },...]
        """
        return self.__run('getmarkethistory', 'public', {'market': market})

    # Market
    def buylimit(self, market, quantity, rate):
        """Used to place a buy order in a specific market.

        Requires API key and secret

        Args:
            market (string): A string for the market (eg: 'btc-eth').
            quantity (float / int / string): The amount to purchase.
            rate (float / int / string): The rate at which to place the order.

        Returns:
            Example:
            {
                "uuid" : "e606d53c-8d70-11e3-94b5-425861b86ab6"
            }
        """
        return self.__run('buylimit', 'market', {'market': market, 'quantity': quantity, 'rate': rate})

    def selllimit(self, market, quantity, rate):
        """Used to place a sell order in a specific market.

        Requires API key and secret

        Args:
            market (string): A string for the market (eg: 'btc-eth').
            quantity (float / int / string): The amount to sell.
            rate (float / int / string): The rate at which to place the order.

        Returns:
            Example:
            {
                "uuid" : "e606d53c-8d70-11e3-94b5-425861b86ab6"
            }
        """
        return self.__run('selllimit', 'market', {'market': market, 'quantity': quantity, 'rate': rate})

    def cancel(self, uuid):
        """Used to cancel a buy or sell order.

        Args:
            uuid (string): The uuid of the order.

        Returns:
            Will return None if successful.
        """

        return self.__run('cancel', 'market', {'uuid': uuid})

    def openorders(self, market=None):
        """ Get all orders that you currently have opened. A specific market can be requested 

        Args:
            market (string, optional): A string for the market (eg: 'btc-eth').

        Returns:
            Example:
            [{
                "Uuid" : null,
                "OrderUuid" : "09aa5bb6-8232-41aa-9b78-a5a1093e0211",
                "Exchange" : "BTC-LTC",
                "OrderType" : "LIMIT_SELL",
                "Quantity" : 5.00000000,
                "QuantityRemaining" : 5.00000000,
                "Limit" : 2.00000000,
                "CommissionPaid" : 0.00000000,
                "Price" : 0.00000000,
                "PricePerUnit" : null,
                "Opened" : "2014-07-09T03:55:48.77",
                "Closed" : null,
                "CancelInitiated" : false,
                "ImmediateOrCancel" : false,
                "IsConditional" : false,
                "Condition" : null,
                "ConditionTarget" : null
            },...]
        """
        if market is None:
            return self.__run('getopenorders', 'market')
        else:
            return self.__run('getopenorders', 'market', {'market': market})

    # Account
    def balance(self, currency=None):
        """Used to retrieve balances from your account. A specific currency can be requested.

        Args:
            currency (string, optional): A string for the currency (eg: 'btc').

        Returns:
            Example:
            [{
                "Currency" : "BTC",
                "Balance" : 14.21549076,
                "Available" : 14.21549076,
                "Pending" : 0.00000000,
                "CryptoAddress" : "1Mrcdr6715hjda34pdXuLqXcju6qgwHA31",
                "Requested" : false,
                "Uuid" : null
            },...]
        """
        if currency is None:
            return self.__run('getbalances', 'account')
        else:
            return self.__run('getbalance', 'account', {'currency': currency})

    def depositaddress(self, currency):
        """Used to retrieve or generate an address for a specific currency. 

        If one does not exist, the call will fail and return ADDRESS_GENERATING until one is available.

        Args:
            currency (string): A string for the currency (eg: 'btc').

        Returns:
            Example:
            {
                "Currency" : "BTC",
                "Address" : "Vy5SKeKGXUHKS2WVpJ76HYuKAu3URastUo"
            }
        """
        return self.__run('getdepositaddress', 'account', {'currency': currency})

    def withdraw(self, currency, quantity, address, paymentid=None):
        """Used to withdraw funds from your account. 

        Please account for transaction fee.

        Args:
            currency (string): A string for the currency (eg: 'btc').
            quantity (float / int / string): The quantity of coins to withdraw.
            address (string): The address where to send the funds.
            paymentid (sring, optional): Used for CryptoNotes/BitShareX/Nxt optional field (memo/paymentid).

        Returns:
            Example:
            {
                    "uuid" : "68b5a16c-92de-11e3-ba3b-425861b86ab6"
            }
        """
        if paymentid is None:
            return self.__run('withdraw', 'account', {'currency': currency, 'quantity': quantity, 'address': address})
        else:
            return self.__run('withdraw', 'account', {'currency': currency, 'quantity': quantity, 'address': address, 'paymentid': paymentid})

    def getorder(self, uuid):
        """Used to retrieve a single order by uuid.

        Args:
            uuid (string): Uuid of the buy or sell order.

        Returns:
            Example:
            {
                "AccountId" : null,
                "OrderUuid" : "0cb4c4e4-bdc7-4e13-8c13-430e587d2cc1",
                "Exchange" : "BTC-SHLD",
                "Type" : "LIMIT_BUY",
                "Quantity" : 1000.00000000,
                "QuantityRemaining" : 1000.00000000,
                "Limit" : 0.00000001,
                "Reserved" : 0.00001000,
                "ReserveRemaining" : 0.00001000,
                "CommissionReserved" : 0.00000002,
                "CommissionReserveRemaining" : 0.00000002,
                "CommissionPaid" : 0.00000000,
                "Price" : 0.00000000,
                "PricePerUnit" : null,
                "Opened" : "2014-07-13T07:45:46.27",
                "Closed" : null,
                "IsOpen" : true,
                "Sentinel" : "6c454604-22e2-4fb4-892e-179eede20972",
                "CancelInitiated" : false,
                "ImmediateOrCancel" : false,
                "IsConditional" : false,
                "Condition" : "NONE",
                "ConditionTarget" : null
            }
        """
        return self.__run('getorder', 'account', {'uuid': uuid})

    def orderhistory(self, market=None):
        """Used to retrieve your order history. A specific market can be requested.

        Args:
            market (string, optional): A string for the market (eg: 'btc-eth').

        Returns:
            Example:
            [{
                "OrderUuid" : "fd97d393-e9b9-4dd1-9dbf-f288fc72a185",
                "Exchange" : "BTC-LTC",
                "TimeStamp" : "2014-07-09T04:01:00.667",
                "OrderType" : "LIMIT_BUY",
                "Limit" : 0.00000001,
                "Quantity" : 100000.00000000,
                "QuantityRemaining" : 100000.00000000,
                "Commission" : 0.00000000,
                "Price" : 0.00000000,
                "PricePerUnit" : null,
                "IsConditional" : false,
                "Condition" : null,
                "ConditionTarget" : null,
                "ImmediateOrCancel" : false
            },...]
        """
        if market is None:
            return self.__run('getorderhistory', 'account')
        else:
            return self.__run('getorderhistory', 'account', {'market': market})

    def withdrawalhistory(self, currency=None):
        """Used to retrieve your withdrawal history. A specific currency can be requested.

        Args:
            currency (string, optional): A string for the currency (eg: 'btc').

        Returns:
            Example:
            [{
                "PaymentUuid" : "b52c7a5c-90c6-4c6e-835c-e16df12708b1",
                "Currency" : "BTC",
                "Amount" : 17.00000000,
                "Address" : "1DeaaFBdbB5nrHj87x3NHS4onvw1GPNyAu",
                "Opened" : "2014-07-09T04:24:47.217",
                "Authorized" : true,
                "PendingPayment" : false,
                "TxCost" : 0.00020000,
                "TxId" : null,
                "Canceled" : true,
                "InvalidAddress" : false
            },...]
        """
        if currency is None:
            return self.__run('getwithdrawalhistory', 'account')
        else:
            return self.__run('getwithdrawalhistory', 'account', {'currency': currency})

    def deposithistory(self, currency=None):
        """Used to retrieve your deposit history. A specific currency can be requested.

        Args:
            currency (string, optional): A string for the currency (eg: 'btc').

        Returns:
            Example:
            [{
                "PaymentUuid" : "554ec664-8842-4fe9-b491-06225becbd59",
                "Currency" : "BTC",
                "Amount" : 0.00156121,
                "Address" : "1K37yQZaGrPKNTZ5KNP792xw8f7XbXxetE",
                "Opened" : "2014-07-11T03:41:25.323",
                "Authorized" : true,
                "PendingPayment" : false,
                "TxCost" : 0.00020000,
                "TxId" : "70cf6fdccb9bd38e1a930e13e4ae6299d678ed6902da710fa3cc8d164f9be126",
                "Canceled" : false,
                "InvalidAddress" : false
            },...]
        """
        if currency is None:
            return self.__run('getdeposithistory', 'account')
        else:
            return self.__run('getdeposithistory', 'account', {'currency': currency})
