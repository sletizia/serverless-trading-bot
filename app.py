from chalice import Chalice
import cbpro
import math
import boto3


# Auth Client
auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS, api_url)

# Public Client
public_client = cbpro.PublicClient()

app = Chalice(app_name='helloworld')

# Globals
stoploss_val = 0.98
exit_position = 1.05


# ----- Helper functions -----

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


# ----- Coinbase API Methods -----

def active_order(pair):
    orders = auth_client.get_orders(product_id=pair)
    order_count = 0
    for i in orders:
        order_count += 1
    if order_count > 0:
        return True
    else:
        return False


def get_current_price(pair):
    # Returns the current price from public coinbase api

    orderbook = public_client.get_product_order_book(pair, level=1)
    current_price = orderbook['asks'][0][0]

    return float(current_price)


def get_balance(pair, accounts):
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


def check_balance(pair, accounts):
    """TODO"""
    pass


def market_buy(pair, stake):
    # Initiates a buy order
    buy = auth_client.buy(funds=stake,
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




init_stop = 0.98 # 2% Risk
trail_stop = 0.99 # 5% Trailing stop exit signal
win_trigger = 1.05 # 5% Reward level

"""# ----- Bot Heartbeat -----
@app.schedule('rate(1 minute)')
def heartbeat(event):
    print("BOTBOIT HEARTBEAT -- I AM ALIVE!")
    accounts = auth_client.get_accounts()
"""
            
    
stake = '0.01' # amount of btc in each position, allocate carefully

@app.route('/buy', methods=['POST'])
def buy():
    request = app.current_request
    webhook_message = request.json_body
    pair = webhook_message["pair"]
    close = webhook_message["close"]

    print("{} BUY SIGNAL INITIATED".format(pair))
    accounts = auth_client.get_accounts()

    balance = get_balance(pair, accounts)
    if balance > check_balance(pair, accounts):
        # No buy happens
        message = "{} Already an active order, no action taken.".format(pair)
        transaction = None
        print("Message: {}".format(message))
        print("Transaction: {}".format(transaction))
        return {"LOG": message,
                "transaction": transaction}
    
    else:
        # Execute a buy
        market_buy(pair, stake)

        set_last_buy_price(pair, close)
        set_last_check_price(pair, close * win_trigger)

        message = "{} Buy signal triggered an execution sequence. A buy was placed and the close price recorded in s3".format(pair)

        print("Message: {}".format(message))
        print("Size: {}".format(balance))
        print("Close: {}".format(close))

        return {"LOG": message,
                "Close": close}


@app.route('/sell', methods=['POST'])
def sell():
    request = app.current_request
    webhook_message = request.json_body
    pair = webhook_message["pair"]
    close = webhook_message["close"]

    print("{} SELL SIGNAL INITIATED".format(pair))
    accounts = auth_client.get_accounts()

    balance = get_balance(pair, accounts)
    if balance > check_balance(pair, accounts):
        # Execute a sell
        sell = market_sell(pair, balance)
        print(sell)
        message = "{} Sell signal triggered an execution sequence. A sell was placed".format(pair)
        
        return {"LOG": message,
                "Close": close}
    