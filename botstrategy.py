from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.trades = []
		self.currentPrice = 0
		self.numSimulTrades = 1

		self.indicators = BotIndicators()

	def tick(self,candlestick):
		self.currentPrice = float(candlestick['weightedAverage'])
		self.prices.append(self.currentPrice)
		
		self.output.log("Price: "+str(candlestick['weightedAverage'])+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			#if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
			if (self.indicators.trend(self.prices,10) == 1):
				self.trades.append(BotTrade(self.currentPrice,stopLoss=0.0001))

		for trade in openTrades:
			#if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
			if (self.indicators.trend(self.prices,10) == 0):
				trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()

"""
Trend: 20 : SL 0.0001 : Proffit : -0.09332981999999873
Trend: 15 : SL 0.0001 : Proffit : -0.08962442000000098
Trend: 10 : SL 0.0001 : Proffit : -0.06183296999999904
"""