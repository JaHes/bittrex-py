import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests


class Bittrex(object):

    def __init__(self, api_key=None, secret=None):
        if api_key and secret is not None:
            self.api_key = api_key
            self.secret = secret

    def __run(self, call, call_type, data={}):
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
        return self.__run('getmarkets', 'public')

    def currencies(self):
        return self.__run('getcurrencies', 'public')

    def ticker(self, market):
        return self.__run('getticker', 'public', {'market': market})

    def marketsummary(self, market=None):
        if market is None:
            return self.__run('getmarketsummaries', 'public')
        else:
            return self.__run('getmarketsummary', 'public', {'market': market})

    def orderbook(self, market, type_):
        return self.__run('getorderbook', 'public', {'market': market, 'type': type_})

    def markethistory(self, market):
        return self.__run('getmarkethistory', 'public', {'market': market})

    # Market
    def buylimit(self, market, quantity, rate):
        return self.__run('buylimit', 'market', {'market': market, 'quantity': quantity, 'rate': rate})

    def selllimit(self, market, quantity, rate):
        return self.__run('selllimit', 'market', {'market': market, 'quantity': quantity, 'rate': rate})

    def cancel(self, uuid):
        return self.__run('cancel', 'market', {'uuid': uuid})

    def openorders(self, market=None):
        if market is None:
            return self.__run('getopenorders', 'market')
        else:
            return self.__run('getopenorders', 'market', {'market': market})

    # Account 
    def balance(self, currency=None):
        if currency is None:
            return self.__run('getbalances', 'account')
        else:
            return self.__run('getbalance', 'account', {'currency': currency})

    def depositaddress(self, currency):
        return self.__run('getdepositaddress', 'account', {'currency': currency})

    def withdraw(self, currency, quantity, address, paymentid=None):
        if paymentid is None:
            return self.__run('withdraw', 'account', {'currency': currency, 'quantity': quantity, 'address': address})
        else:
            return self.__run('withdraw', 'account', {'currency': currency, 'quantity': quantity, 'address': address, 'paymentid': paymentid})

    def getorder(self, uuid):
        return self.__run('getorder', 'account', {'uuid': uuid})

    def orderhistory(self, market=None):
        if market is None:
            return self.__run('getorderhistory', 'account')
        else:
            return self.__run('getorderhistory', 'account', {'market': market})

    def withdrawalhistory(self, currency=None):
        if currency is None:
            return self.__run('getwithdrawalhistory', 'account')
        else:
            return self.__run('getwithdrawalhistory', 'account', {'currency': currency})

    def deposithistory(self, currency=None):
        if currency is None:
            return self.__run('getdeposithistory', 'account')
        else:
            return self.__run('getdeposithistory', 'account', {'currency': currency})
