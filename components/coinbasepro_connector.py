import cbpro
import math


class CBProConnector:
    def __init__(self, config_settings):

        API_SECRET = config_settings["apiSecret"]
        API_KEY = config_settings["apiKey"]
        API_PASS = config_settings["apiPass"]
        api_url = config_settings["apiUrl"]

        self.stake = config_settings["stakeBTC"]
        self.account_ids = config_settings["accountIds"]

        # Auth Client
        self.auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS, api_url)

        # Public Client
        self.public_client = cbpro.PublicClient()

    # ----- Helper functions -----

    def truncate(self, n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier


    # ----- Coinbase API Methods -----

    def get_current_price(self, pair):
        # Returns the current price from public coinbase api

        orderbook = self.public_client.get_product_order_book(pair, level=1)
        current_price = orderbook['asks'][0][0]

        return float(current_price)
    

    def get_account_ids(self):
        # TODO: get account ids from api rather than passing from config
        # would allow balance check of any asset or pair not just ones that 
        # have an id recorded manually
        pass


    def get_balance(self, pair):
        accounts = self.auth_client.get_accounts()
        pair_id = self.account_ids[pair]
        for i in accounts:
            if i['id'] == pair_id:
                balance = i['balance']
        # each pair needs to be truncated to a different decimal place
        # number is based on the base tick size here:  https://pro.coinbase.com/markets
        if pair == 'LINK-BTC':
            return self.truncate(float(balance), 3)
        elif pair == 'XLM-BTC':
            return self.truncate(float(balance))
        elif pair == 'ATOM-BTC':
            return self.truncate(float(balance), 2)
        elif pair =='ZRX-BTC':
            return self.truncate(float(balance), 6)
        elif pair =='LTC-BTC':
            return self.truncate(float(balance), 9)
        elif pair =='ETH-BTC':
            return self.truncate(float(balance), 9)
        elif pair =='ETC-BTC':
            return self.truncate(float(balance), 9)
        elif pair =='BCH-BTC':
            return self.truncate(float(balance), 9)
        elif pair =='ADA-BTC':
            return self.truncate(float(balance), 3)
        elif pair =='MKR-BTC':
            return self.truncate(float(balance), 6)
        elif pair =='OMG-BTC':
            return self.truncate(float(balance))
        elif pair =='ZEC-BTC':
            return self.truncate(float(balance), 5)
        elif pair =='FIL-BTC':
            return self.truncate(float(balance), 4)
        else:
            print("PAIR INVALID or something like that")
            return(1000)

    # ----- Order Execution Methods -----

    def market_buy_stake(self, pair):
        # Initiates a buy order
        buy = self.auth_client.buy(funds=self.stake,
                order_type='market',
                product_id=pair)
        print("{} BUY EXECUTED: {}".format(pair, buy))


    def market_sell_all(self, pair, balance):
        sell = self.auth_client.sell(size=balance,
                                        order_type='market',
                                        product_id=pair)
        print("{} SELL EXECUTED: {}".format(pair, sell))


    def take_profits(pair):
        #TODO: implement to sell the profit percentage of a position
        pass

if __name__ == "__main__":
    # Load Config
    from config_reader import ConfigReader
    cf = ConfigReader()
    cbpro_config = cf.load_config_from_file("../config.json")["cbpro"]

    cbpro = CBProConnector(cbpro_config)

    # Test Variables
    test_pair = 'ETH-BTC'
    test_stakeBTC = '0.0001'

    # Test 1 - Helper functions
    print("__TEST 1__")
    num = 0.12345678
    print("Truncate {}".format(num))
    num = cbpro.truncate(num, 3)
    print("Truncated to 3 spaces: {}".format(num))

    # Test 2 - get current price of a pair
    print("__TEST 2__")
    cur_price = cbpro.get_current_price(test_pair)
    print("Current price of {}: {}".format(test_pair, cur_price))

    # Test 3 - get balance of a pair
    print("__TEST 3__")
    balance = cbpro.get_balance(test_pair)
    print("Balance of {}: {}".format(test_pair, balance))

    #Test 4 - Execute Buy
    #print("__TEST 4__")
    #cbpro.market_buy_stake(test_pair)

    #Test 5 - Execute Sell
    #print("__TEST 5__")
    #cbpro.market_sell_all(test_pair, balance)


    