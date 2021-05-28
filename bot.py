import requests
import time
import sqlite3
import json
import hmac
import hashlib

# =======================================================
# ===       INIT                                      ===
# =======================================================

database = sqlite3.connect('./botRecords.db')
dbMutation = database.cursor()

binanceAPI = "https://api.binance.com/api/v3/"
tickersBinance = []
tickersKraken = []
intervalPrice = []

intervalStart = int(time.time())

# Check if table exists
dbMutation.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='history' ''')
if dbMutation.fetchone()[0]==1:
    print('[INIT] Table exists.')
else:
    dbMutation.execute('''CREATE TABLE history ([ID] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, [exchange] TEXT NOT NULL, [ticker] TEXT NOT NULL, [time] TEXT  NOT NULL, [dip] INTEGER)''')
    print('[INIT] Table created.')

# Read configuration
with open('configuration.json') as config:
    data = json.load(config)
    
    # Populate ticker arrays
    # Binance
    if (data["exchanges"]["binance"]["enabled"]):
        for i in range(len(data["exchanges"]["binance"]["tickers"])):
            tickersBinance.append(data["exchanges"]["binance"]["tickers"][i])
    
    # Kraken
    if (data["exchanges"]["kraken"]["enabled"]):
        for i in range(len(data["exchanges"]["kraken"]["tickers"])):
            tickersKraken.append(data["exchanges"]["kraken"]["tickers"][i])
        
    # Read misc config
    interval = data["dip_config"]["interval"]
    #dipThreshold = data["dip_config"]["threshold"]
    #dipThreshold = -dipThreshold
    dipThreshold = 5

# =======================================================
# ===       FUNC                                      ===
# =======================================================

def hash(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def storeIntoDB(exchange, ticker, time, dip):
    # Store stuff into table
    dbMutation.execute("INSERT INTO history VALUES ('" + exchange + "', '" + ticker + "', '" + time + "', '" + dip + "')")
    dbMutation.commit()
    
def getTime():
    return time.strftime("%H:%M:%S", time.localtime())

def newInterval():
    print(getTime() + " [INFO] New interval!")
    intervalStart = int(time.time())

    # Populate intervalPrice[] after clearing it
    intervalPrice.clear()

    if (data["exchanges"]["binance"]["enabled"]):
        for i in range(len(tickersBinance)):
            intervalPrice.append( basePrice( 'Binance', tickersBinance[i], int(float(binance.getPrice(tickersBinance[i]))), False ) )
                
# Classes
class Binance:    
    # Acquire price    
    def getPrice(self, ticker):
        response = requests.get(binanceAPI + str("ticker/price?symbol=") + str(ticker))
        
        # Handle response
        if response.status_code == 200:
            return response.json()['price']
        else:
            return getTime() + "ERROR: " + str(response.status_code)
    
    def buy(self, ticker):
        # Assemble parameter string
        stake = data["exchanges"]["binance"]["stake"]
        paramString = "symbol=" + str(ticker) + "&side=BUY&type=MARKET&quoteOrderQty=" + str(stake) + "&timestamp=" + str(int(time.time() * 1000))
        paramString = paramString + "&signature=" + str(hash(paramString, data["exchanges"]["binance"]["api_secret"]))
        
        fullRequest = binanceAPI + "order?" + paramString
        print(getTime() + " [INFO] " + fullRequest)
        
        print()
        
        # Send POST
        headers = {'X-MBX-APIKEY': data["exchanges"]["binance"]["api_key"]}
        response = requests.post(fullRequest.encode(), headers=headers)
        
        # Handle response
        if response.status_code == 200:
            return getTime() + " [BUY\u2705] SUCCESS: " + str(response.status_code) + " - "+ str(response.json()), True
        else:
            return getTime() + " [BUY\u274C] ERROR: " + str(response.status_code) + " - " + str(response.json()), False

# Object to use as a base price for all intervals
class basePrice:
    def __init__(self, exchange, ticker, price, bought):
        self.exchange = exchange
        self.ticker = ticker
        self.price = price
        self.bought = bought
        

# Create instances
binance = Binance()

# =======================================================
# ===       MAIN                                      ===
# =======================================================

# Acquire prices
print(getTime() + " [INFO] Interval set at: " + str(interval) + " seconds.")
print(getTime() + " [INFO] Percentage threshhold: " + str(dipThreshold) + "%")
print(getTime() + " [LOOP] Beginning...")
newInterval()

while True:
    time.sleep(1)
    
    # Check if an interval has passed
    if (int(time.time()) - intervalStart) > interval:
        newInterval()
 
    #for obj in intervalPrice:
    #    print( obj.exchange, obj.ticker, obj.price, sep =' ' )
        
    # Always get the new prices
    print(getTime() + " [PRIC] Querying binance...")
    if (data["exchanges"]["binance"]["enabled"]):
        for i in range(len(tickersBinance)):
            priceNow = int(float(binance.getPrice(tickersBinance[i])))

            # Check if the price is below the dip threshold
            # formula to calculate percentage change: 100 * (NEW_PRICE - OLD_RPICE) / OLD_PRICE
            for base in intervalPrice:
                if base.exchange == "Binance" and base.ticker == tickersBinance[i]:
                    percentage = 100 * (priceNow - base.price) / base.price
                    print(getTime() + "   > " + tickersBinance[i] + ": " + str(priceNow) + " - change: " + str(round(percentage, 2)) + "%")
                    
                    # Buy if the price has dipped below threshold and nothing has been bought before
                    if percentage < dipThreshold and not base.bought:
                        print(getTime() + "       > Percentage below threshold, buying!")
                        
                        msg, status = binance.buy(base.ticker)
                        print(msg)
                        
                        # Only set flag if binance did not return an error
                        if status:
                            storeIntoDB("Binance", tickersBinance[i], getTime(), percentage)
                            base.bought = True
                        