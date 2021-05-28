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
    dipThreshold = data["dip_config"]["threshold"]
    dipThreshold = -dipThreshold

# =======================================================
# ===       FUNC                                      ===
# =======================================================

def hashing(query_string):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def storeIntoDB(exchange, ticker, time, dip):
    # Store stuff into table
    dbMutation.execute("INSERT INTO history VALUES ('" + exchange + "', '" + ticker + "', '" + time + "', '" + dip + "')")
    dbMutation.commit()
    
def getTime():
    return time.strftime("%H:%M:%S", time.localtime())

# Classes
class Binance:    
    # Acquire price    
    def getPrice(self, ticker):
        response = requests.get(binanceAPI + str("ticker/price?symbol=") + str(ticker))
        
        # Handle response
        if not response.status_code == 200:
            return "ERROR: " + response.status_code
        else:
            return response.json()['price']

# Object to use as a base price for all intervals
class basePrice:
    def __init__(self, exchange, ticker, price):
        self.exchange = exchange
        self.ticker = ticker
        self.price = price
            
    def report(self):
        print(self)
        

# Create instances
binance = Binance()

# =======================================================
# ===       MAIN                                      ===
# =======================================================

# Acquire prices
print(getTime() + " [INFO] Interval set at: " + str(interval) + " seconds.")
print(getTime() + " [LOOP] Beginning...")
freshInterval = True
intervalStart = int(time.time())
haveBought = False

while True:
    time.sleep(1)
    
    # Check if an interval has passed
    if (int(time.time()) - intervalStart) > interval:
        freshInterval = True
        haveBought = False
        intervalStart = int(time.time())
        
    # Save price at start of interval
    if freshInterval:
        print(getTime() + " [INFO] New interval!")
        
        # Populate intervalPrice[]
        if (data["exchanges"]["binance"]["enabled"]):
            for i in range(len(tickersBinance)):
                intervalPrice.append( basePrice('Binance', tickersBinance[i], int(float(binance.getPrice(tickersBinance[i])))) )
        
        freshInterval = False
 
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
                    if percentage < dipThreshold and not haveBought:
                        print(getTime() + "       > Percentage below threshold, buying!")
                        haveBought = True