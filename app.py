from chalice import Chalice
import cbpro
import math

# Componenent Imports
from components.config_reader import ConfigReader
from components.s3_connector import S3Connector
from components.coinbasepro_connector import CBProConnector


app = Chalice(app_name='tradingbot')

cf = ConfigReader()
config_values = cf.load_config_from_file("config.json")

s3 = S3Connector(config_values["s3"])
cbpro = CBProConnector(config_values["cbpro"])

# ----- Bot Heartbeat -----
@app.schedule('rate(1 minute)')
def heartbeat(event):
    print("BOTBOIT HEARTBEAT -- HELLO I AM ALIVE!")
    accounts = auth_client.get_accounts()


@app.route('/buy_crypto', methods=['POST'])
def buy():
    request = app.current_request
    webhook_message = request.json_body
    pair = webhook_message["pair"]
    close = webhook_message["close"]

    print("{} BUY SIGNAL RECEIVED".format(pair))
    balance = cbpro.get_balance(pair)
    if balance > 0.001: # not zero incase there are a few cents left after a trade
        # If we are already holding the coin we don't buy more
        message = "{} Already holding coin, no action taken.".format(pair)
        transaction = None
        print("Message: {}".format(message))
        print("Transaction: {}".format(transaction))
        return {"LOG": message,
                "transaction": transaction}
    
    else:
        # Execute a buy
        cbpro.market_buy_stake(pair)
        s3.set_last_buy_price(pair, close)
        message = "{} Buy executed at {}"

        print("Message: {}".format(message))
        print("Size: {}".format(balance))
        print("Close: {}".format(close))

        return {"LOG": message,
                "Close": close}


@app.route('/sell_crypto', methods=['POST'])
def sell():
    request = app.current_request
    webhook_message = request.json_body
    pair = webhook_message["pair"]
    close = webhook_message["close"]

    print("{} SELL SIGNAL RECEIVED".format(pair))

    balance = cbpro.get_balance(pair)
    if balance > 0.001:
        # If we are holding the coin we sell
        cbpro.market_sell_all(pair)
        message = "{} Sell executed at {}".format(pair)
        
        return {"LOG": message,
                "Close": close}