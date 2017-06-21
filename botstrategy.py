from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
#from botpublic import BotPublic 

from poloniex import Poloniex
polo = Poloniex()
ticker = polo.returnTicker()

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.trades = []
		self.currentPrice = None
		self.numSimulTrades = 1
		self.stopLoss = 0.00001
		self.indicators = BotIndicators()


	def tick(self,candlestick):
		self.currentPrice = float(candlestick['weightedAverage'])
		self.currentVolume = float(candlestick['volume'])
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
			#if (float(ticker['BTC_ZEC']['percentChange']) < 0):
			if (self.indicators.trend(self.prices,self.trendPeriod) == 1 and self.currentVolume > self.minVolume):
					self.trades.append(BotTrade(self.currentPrice,stopLoss=self.stopLoss))

		for trade in openTrades:
			#if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
			if (self.indicators.trend(self.prices,self.trendPeriod) == 0 and self.currentVolume > self.minVolume):
					trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()

