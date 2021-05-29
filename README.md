# Buy the dip
Are you tired of missing out on *juicy* dips when you're...
 - ...sleeping?  
 - ...at work?
 - ...not checking the prices for 5 minutes?

Do you want to outsource your DCA strategy to a computer?

Then this bot is for **you**!  

It is very simple and follows the true tried-and-tested investment strategy as preached by Warren Buffet:  
![](https://i.imgur.com/olZZatY.png)

## What does this thing do exactly?
Basically, the bot monitors user-defined tickers on various exchanges for a price change within a given timeframe.  

At the start of said timeframe, the bot saves the current price of all tickers it is monitoring.  
Each second, the bot will then pull the prices for each ticker and compares them to the starting price.  
*It calculates the price change as a percentage.*

If the price change in percentage is below a user-defined threshold, then the bot will attempt to buy the ticker that dropped.  
Once the timeframe ends, a new starting price gets saved.

**Important:** The timeframe starts **at the very the moment** the bot runs.  
It is *not* getting the price data of the last *n* seconds, because the bot does not acquire historical price data.

## Features
 - Multi exchange support
    - Binance
    - Kraken
    - Coinbase `pending`
 - Discord integration
 - Extensive configuration

## Installation and usage
Please refer to the [wiki](https://github.com/ThisIsntTheWay/buy-the-dip/wiki) for installation and usage of this bot.
  
#### ToDo
- [X] Implement support for binance
- [X] Implement support for kraken
- [ ] Implement support for coinbase
- [X] Implement buy logic
- [ ] Add "tiered" dip mode
- [X] Add discord integration
- [ ] Add sqlite db
