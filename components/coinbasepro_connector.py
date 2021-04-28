import cbpro
import math
from config_reader import ConfigReader


class CBProConnector:
    def __init__(self, config_settings):

        API_SECRET = config_settings["apiSecret"]
        API_KEY = config_settings["apiKey"]
        API_PASS = config_settings["apiPass"]
        api_url = config_settings["apiUrl"]

        self.stake = config_settings["stakeBTC"]

        # Auth Client
        self.auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS, api_url)

        # Public Client
        self.public_client = cbpro.PublicClient()

    # ----- Helper functions -----

    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier


    # ----- Coinbase API Methods -----

    def get_current_price(self, pair):
        # Returns the current price from public coinbase api

        orderbook = self.public_client.get_product_order_book(pair, level=1)
        current_price = orderbook['asks'][0][0]

        return float(current_price)


    def get_balance(self, pair):
        accounts = self.auth_client.get_accounts()
        pair_id = account_ids[pair]
        for i in accounts:
            if i['id'] == pair_id:
                balance = i['balance']
        # each pair needs to be truncated to a different decimal place
        # number is based on the base tick size here:  https://pro.coinbase.com/markets
        if pair == 'LINK-BTC':
            return truncate(float(balance), 3)
        elif pair == 'XLM-BTC':
            return truncate(float(balance))
        elif pair == 'ATOM-BTC':
            return truncate(float(balance), 2)
        elif pair =='ZRX-BTC':
            return truncate(float(balance), 6)
        elif pair =='LTC-BTC':
            return truncate(float(balance), 9)
        elif pair =='ETH-BTC':
            return truncate(float(balance), 9)
        elif pair =='ETC-BTC':
            return truncate(float(balance), 9)
        elif pair =='BCH-BTC':
            return truncate(float(balance), 9)
        elif pair =='ADA-BTC':
            return truncate(float(balance), 3)
        elif pair =='MKR-BTC':
            return truncate(float(balance), 6)
        elif pair =='OMG-BTC':
            return truncate(float(balance))
        elif pair =='ZEC-BTC':
            return truncate(float(balance), 5)
        elif pair =='FIL-BTC':
            return truncate(float(balance), 4)
        else:
            print("PAIR INVALID or something like that")
            return(1000)



    def market_buy(self, pair):
        # Initiates a buy order
        buy = auth_client.buy(funds=self.stake,
                order_type='market',
                product_id=pair)
        print("{} BUY EXECUTED".format(pair))
        print(buy)


    def market_sell(pair, balance):
        sell = auth_client.sell(size=balance,
                                        order_type='market',
                                        product_id=pair)
        print("{} SELL EXECUTED".format(pair))
        print(sell)


if __name__ == "__main__":
    # Load Config
    from config_reader import ConfigReader
    cf = ConfigReader()
    cbpro_config = cf.load_config_from_file("../config.json")["cbpro"]

    cbpro = CBProConnector(cbpro_config)

    # Test Variables
    test_pair = 'BTC-USD'

    # Test 1 - get current price of a pair
    cur_price = cbpro.get_current_price(test_pair)
    print("Current price of {}: {}".format(test_pair, cur_price))

    