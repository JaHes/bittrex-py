import requests
import urllib
import time
import hmac
import hashlib

#Calls stored in arrays for checking later
public_calls = ['getmarkets', 'getcurrencies', 'getticker', 'getmarketsummaries', 'getmarketsummary', 'getorderbook', 'getmarkethistory']
market_calls = ['buylimit', 'selllimit', 'cancel', 'getopenorders']
account_calls = ['getbalances', 'getbalance', 'getdepositaddress', 'withdraw', 'getorder', 'getorderhistory', 'getwithdrawalhistory', 'getdeposithistory']

class Bittrex(object):

    def __init__(self, api_key=None, secret=None):
        #Assign api_key and secret if they are not left blank
        self.api_key = api_key if api_key is not None else ''
        self.secret = secret if secret is not None else ''

    def __run(self, call, data={}):
        #Generate specified url
        if call in public_calls:
            url = 'https://bittrex.com/api/v1.1/public/'
        elif call in market_calls:
            url = 'https://bittrex.com/api/v1.1/market/'
        elif call in account_calls:
            url = 'https://bittrex.com/api/v1.1/account/'
        else:
            return 'Oops'

        #Append values to url
        url += '%s?%s' % (call, urllib.parse.urlencode(data))

        #Check if api key is required
        if call not in public_calls:
            #Append values to url
            url += '&apikey=%s' % self.api_key
            url += '&nonce=%s' % time.time()
            #Generate header hash
            b_secret = bytes(self.secret, 'latin-1')
            b_url = bytes(url, 'latin-1')
            sig = hmac.new(b_secret, b_url, hashlib.sha512).hexdigest()
            header = {'apisign': sig}
            #Get with header
            r_get = requests.get(url, headers=header)
        else:
            #No header needed if a public call
            r_get = requests.get(url)

        #request to json
        r_json = r_get.json()

        #Check if there was a result
        if r_json['result']:
            return r_json['result']
        else:
            return r_json['message']

    #Public
    def markets(self):
        return self.__run('getmarkets')

    def currencies(self):
        return self.__run('getcurrencies')

    def ticker(self, market):
        return self.__run('getticker', {'market': market})

    def marketsummary(self, market=None):
        if market is None:
            return self.__run('getmarketsummaries')
        else:
            return self.__run('getmarketsummary', {'market': market})

    def orderbook(self, market, type_):
        return self.__run('getorderbook', {'market': market, 'type': type_})

    def markethistory(self, market):
        return self.__run('getmarkethistory', {'market': market})

    #Market
    def buylimit(self, market, quantity, rate):
        return self.__run('buylimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def selllimit(self, market, quantity, rate):
        return self.__run('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})

    def cancel(self, uuid):
        return self.__run('cancel', {'uuid': uuid})

    def openorders(self, market=None):
        if market is None:
            return self.__run('getopenorders')
        else:
            return self.__run('getopenorders', {'market': market})

    #Account 
    def balance(self, currency=None):
        if currency is None:
            return self.__run('getbalances')
        else:
            return self.__run('getbalance', {'currency': currency})

    def depositaddress(self, currency):
        return self.__run('getdepositaddress', {'currency': currency})

    def withdraw(self, currency, quantity, address, paymentid=None):
        if paymentid is None:
            return self.__run('withdraw', {'currency': currency, 'quantity': quantity, 'address': address})
        else:
            return self.__run('withdraw', {'currency': currency, 'quantity': quantity, 'address': address, 'paymentid': paymentid})

    def getorder(self, uuid):
        return self.__run('getorder', {'uuid': uuid})

    def orderhistory(self, market=None):
        if market is None:
            return self.__run('getorderhistory')
        else:
            return self.__run('getorderhistory', {'market': market})

    def withdrawalhistory(self, currency=None):
        if currency is None:
            return self.__run('getwithdrawalhistory')
        else:
            return self.__run('getwithdrawalhistory', {'currency': currency})

    def deposithistory(self, currency=None):
        if currency is None:
            return self.__run('getdeposithistory')
        else:
            return self.__run('getdeposithistory', {'currency': currency})
