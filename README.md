# Serverless-Trading-Bot
Automated Serverless Crypto Currency and Stock Trading Bot

## Introduction
This project uses serverless aws lambda functions to create an api to trade assets. Use TradingView or programmatically make trades based on certain conditions. 

Currently includes a connector for the Coinbase Pro API to trade crypto currencies. 
In the works is a connector for Alpaca trading API which will allow you to trade stocks as well.

By integrating TradingView you can set buy and sell signals based on whatever indicators or market conditions you want. 
You can create a fully automated trading bot that buys and sells assets, although this is not recommended* (see disclaimer).

### Requirements
  1. Python
  2. Install and Configure [Chalice](https://aws.github.io/chalice/index.html)
  3. [AWS](https://aws.amazon.com/) Account (optional if you want to deploy the bot live)
  4. [TradingView](https://www.tradingview.com/) for Alert Triggers (or other trigger sources with webhooks)
  5. [Coinbase Pro](https://pro.coinbase.com/) account and api key
  6. [Alpaca Trading API](https://app.alpaca.markets/) **Implementation Coming Soon


## Installation
  1. First, [create a new Chalice project](https://aws.github.io/chalice/quickstart.html#creating-your-project)
  2. Clone the repo inside the new project directory
    
  ```bash
  cd 'Project directory name'
  git clone https://github.com/sletizia/serverless-trading-bot.git
  ```
  3. Move the repo files from its folder to the project foler, overwrite/replace chalice files with the repo files

  ```bash
  mv serverless-trading-bot/* .
  ```
  
  4. Make sure the chalice project runs locally
  ```bash
  chalice local
  ```

## Config
The config.json file is where you put your coinbase pro and alpaca api keys, trading account information, AWS S3 info and other configuration settings coming in the future. 
Json Schema:
```json
{
    "cbpro": {
        "apiKey": "",
        "apiPass": "",
        "apiSecret": "",
        "apiUrl": "",
        "accountIds": {"ETH-BTC": "example-account-id"},
        "stakeBTC": "0.0"
    },
    "s3": {
        "bucketName": ""
    },
    "alpaca": {
        "apiKey": "",
        "apiPass": "",
        "apiSecret": ""
    }
}
```
the `accountIds: {}` element needs to be populated manually right now. To do that use the "get_accounts()" method from the cbpro package in the python cmd line console. You need your api key information for this step as well:
```bash
python3
```

```python
import cbpro

API_KEY="YOUR API KEY"
API_SECRET="YOUR API SECRET"
API_PASS="YOUR API PASSWORD"
API_URL="https://api.pro.coinbase.com"

auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS, API_URL)
auth_client.get_accounts()
```
`auth_client.get_accounts()` returns a list of each of your crypto currency accounts with their id's. Pick the currencies you want to trade, extract the id, and add it to the config.json file

## Components



## Investment Disclaimer
All investment strategies and investments involve risk of loss.  Nothing contained in this readme should be construed as investment advice.  Any reference to an investment’s or bot's past or potential performance is not, and should not be construed as, a recommendation or as a guarantee of any specific outcome or profit. You should always monitor your investements. Only use this implementation in a live trading setting if you know what you are doing and are prepared to potentially lose your investment.

