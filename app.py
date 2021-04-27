from chalice import Chalice
import cbpro
import math
import boto3

# ----- GLOBALS -----
# TODO: Make this stuff more secure you dum dum
API_SECRET = "zH+0NaE/9FMtF5HK5bEv2u+oFdXbjNNCKnx+Iq6P7lM16ybWPRW1tFmhYArXCoFB0W12qJA8jso/G5mTQ3suKg=="
API_KEY = "382fe2a34363b8d4d937c61cdcbc8a59"
API_PASS = "g74zbn0mkic"
api_url = 'https://api.pro.coinbase.com'

# Auth Client
auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS, api_url)

# Public Client
public_client = cbpro.PublicClient()

app = Chalice(app_name='helloworld')

# Globals
stoploss_val = 0.98
exit_position = 1.05


account_ids = {
    'LINK-BTC': 'b9967609-3379-4f48-a126-9e816e9ff625',
    'XLM-BTC': 'da47bc6a-9a69-476c-ba37-ff57e338bd20',
    'ATOM-BTC': 'fb2984b4-bd06-4b25-a735-37bc9cc19ffd',
    'ZRX-BTC': '8357d81c-8a66-46ea-a9a8-500fa4f1733b',
    'ADA-BTC': '3071fd8a-e326-4217-a478-b345cdae67f1',
    'ETH-BTC': '058efe2d-97ff-49fc-a92b-77eb61e8ec76',
    'FIL-BTC': '690a7ab3-3fe3-4696-baab-0400e31a92b4',
    'MKR-BTC': '15bd9ea0-6e23-4357-b894-7f080cb29578',
    'OMG-BTC': 'fe49d4b2-38cc-43c6-807b-5952054b0d7e',
    'ZEC-BTC': '8d20086f-b60c-4c67-ac4d-3d348c28fd89',
    'ETC-BTC': 'cb653b55-19a4-412a-8b08-8fdfeb6489e6',
    'BCH-BTC': 'b089ad31-1756-40c5-8153-d9330efc68a3',
    'LTC-BTC': '4e507a70-b055-473a-abc0-3210c608d9b2'
}

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
    balance = get_balance(pair, accounts)
    
    if pair == 'XLM-BTC': 
        balance_check_val = 100
    elif pair == 'LINK-BTC':
        balance_check_val = 1
    elif pair == 'ATOM-BTC':
        balance_check_val = 1
    elif pair == 'ZRX-BTC':
        balance_check_val = 100
    elif pair == 'LTC-BTC':
        balance_check_val = 1
    elif pair == 'ETH-BTC':
        balance_check_val = 0.1
    elif pair == 'ETC-BTC':
        balance_check_val = 10
    elif pair == 'BCH-BTC':
        balance_check_val = 0.1
    elif pair == 'ADA-BTC':
        balance_check_val = 100
    elif pair == 'MKR-BTC':
        balance_check_val = 0.1
    elif pair == 'OMG-BTC':
        balance_check_val = 10
    elif pair == 'ZEC-BTC':
        balance_check_val = 1
    elif pair == 'FIL-BTC':
        balance_check_val = 1

    return balance_check_val


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


# ----- S3 Value Storage Methods -----

def get_last_buy_price(pair):
    # Returns float value of last buy price for pair
    bucket_name = "botboibucket"
    s3_path = pair + "/last_buy_price"
    s3 = boto3.resource("s3")
    ob = s3.Object(bucket_name, s3_path)
    last_buy_price = ob.get()['Body'].read().decode('utf-8')
    return float(last_buy_price)


def set_last_buy_price(pair, close):
    # Stores value of last buy price for pair
    bucket_name = "botboibucket"
    s3_path = pair + "/last_buy_price"
    s3 = boto3.resource("s3")
    encoded_string = str(close).encode("utf-8")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)


def set_last_sell_price(pair, close):
    # Stores value of last buy price for pair
    bucket_name = "botboibucket"
    s3_path = pair + "/last_sell_price"
    s3 = boto3.resource("s3")
    encoded_string = str(close).encode("utf-8")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)


def get_last_check_price(pair):
    # Returns float value of last check price for pair
    bucket_name = "botboibucket"
    s3_path = pair + "/last_check_price"
    s3 = boto3.resource("s3")
    ob = s3.Object(bucket_name, s3_path)
    last_check_price = ob.get()['Body'].read().decode('utf-8')
    return float(last_check_price)


def set_last_check_price(pair, checkprice):
    # Stores value of last buy price for pair
    bucket_name = "botboibucket"
    s3_path = pair + "/last_check_price"
    s3 = boto3.resource("s3")
    encoded_string = str(checkprice).encode("utf-8")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)



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
    