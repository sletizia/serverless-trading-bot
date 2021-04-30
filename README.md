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


## Investment Disclaimer
All investment strategies and investments involve risk of loss.  Nothing contained in this readme should be construed as investment advice.  Any reference to an investment’s or bot's past or potential performance is not, and should not be construed as, a recommendation or as a guarantee of any specific outcome or profit. You should always monitor your investements. Only use this implementation in a live trading setting if you know what you are doing and are prepared to potentially lose your investment.

