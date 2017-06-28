# Use the previous 10 bars' movements to predict the next movement.

# Use a random forest classifier. More here: http://scikit-learn.org/stable/user_guide.html
from sklearn.ensemble import RandomForestClassifier
from collections import deque
import numpy as np

from poloniex import Poloniex
import time, datetime

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

conn = Poloniex()

security = 'BTC_ZEC'
window_length = 5 # Amount of prior bars to study
	
classifier = RandomForestClassifier() # Use a random forest classifier

# deques are lists with a maximum length where old entries are shifted out
recent_prices = deque(maxlen=window_length+2) # Stores recent prices
X = deque(maxlen=500) # Independent, or input variables
Y = deque(maxlen=500) # Dependent, or output variable


numSimulTrades = 1

period = 300
Days = 10

startTime = time.time() - (86400 * Days)
endTime = time.time() #End at current time

data = conn.returnChartData(security, period, startTime, endTime)

All_trades = []


class BotTrade(object):
	def __init__(self,currentPrice):
		self.status = "OPEN"
		self.entryPrice = currentPrice
		self.exitPrice = 0

	def close(self,currentPrice):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		print("Closed at : " + str(self.exitPrice))


prediction = 0 # Stores most recent prediction
	
	#schedule_function(rebalance, date_rules.every_day(), time_rules.market_close(minutes=5))
	#schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())


def datetime_from_timestamp(timestamp):
	x = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	return x


def rebalance(data):
	openTrades = []
	for trade in All_trades:
		if (trade.status == "OPEN"):
			openTrades.append(trade)

	#recent_prices.append(float(data['weightedAverage'])) # Update the recent prices # 10.40812181999999
	recent_prices.append(float(data['close'])) # 
	if len(recent_prices) == window_length+2: # If there's enough recent price data
		
		# Make a list of 1's and 0's, 1 when the price increased from the prior bar
		changes = np.diff(recent_prices) > 0
		
		X.append(changes[:-1]) # Add independent variables, the prior changes
		Y.append(changes[-1]) # Add dependent variable, the final change
		

		if len(Y) >= 100: # There needs to be enough data points to make a good model
			classifier.fit(X, Y) # Generate the model
			prediction = classifier.predict(changes[1:]) # Predict
			# If prediction = 1, buy all shares affordable, if 0 sell all shares
			#order_target_percent(security, prediction)

			print(str(datetime_from_timestamp(data['date'])) + " : Price = " + str(recent_prices[-1]))
			if prediction == True:
				if (len(openTrades) < numSimulTrades):
					print('BUY')
					All_trades.append(BotTrade(recent_prices[-1]))
					#self.trades.append(BotTrade(self.currentPrice,stopLoss=self.stopLoss))
			else:
				print('CLOSE')
				for trades in openTrades:
					trades.exitPrice = recent_prices[-1]
					trades.status = "CLOSED"



for i in data:
	rebalance(i)

total = []
for trade in All_trades:
	if trade.status == "CLOSED":
		#total.append(float(trades.entryPrice) - float(recent_prices[-1]))
		total.append(float(trade.exitPrice) - float(trade.entryPrice))

		profit = float(trade.exitPrice) - float(trade.entryPrice)

		if float(trade.exitPrice > float(trade.entryPrice)):
			print(bcolors.OKGREEN + str(format(profit, '.6f')) + "\t" + str(trade.status) + bcolors.ENDC)

		else:
			print(bcolors.FAIL + str(format(profit, '.6f')) + "\t" + str(trade.status) + bcolors.ENDC)


print(sum(total))
