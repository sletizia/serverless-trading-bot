from chalice import Chalice
import cbpro
import math


app = Chalice(app_name='tradingbot')

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

    print("{} BUY SIGNAL RECEIVED".format(pair))
    
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
    