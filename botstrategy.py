from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade


SL = 0.00001
TP = 0

TrendPeriod = 10 #11 SubTotal: -3.68487624 #10 SubTotal: -5.3347665

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.trades = []
		self.currentPrice = ""
		self.numSimulTrades = 1

		self.indicators = BotIndicators()

	def tick(self,candlestick):
		self.currentPrice = float(candlestick['weightedAverage'])
		self.currentVolume = float(candlestick['volume'])
		self.prices.append(self.currentPrice)

		self.output.log("Price: "+str(candlestick['weightedAverage'])+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15))+"\t Volume: "+str(self.currentVolume)+"\t Trend: " + str(self.indicators.trend(self.prices,TrendPeriod)))

		self.evaluatePositions()

		self.showPositions()

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			
			#if (self.currentPrice < self.indicators.movingAverage(self.prices,20) and self.currentPrice < self.indicators.movingAverage(self.prices,60)):
			#if (self.indicators.movingAverage(self.prices,10) == self.indicators.movingAverage(self.prices,20) and self.indicators.trend(self.prices,TrendPeriod) == 1):
			#if (self.currentPrice > self.indicators.movingAverage(self.prices,10) and self.currentVolume > 20):
			#if (self.currentPrice > self.indicators.movingAverage(self.prices,10) and self.indicators.trend(self.prices,10) == 1):
			#if (self.currentPrice < self.indicators.movingAverage(self.prices,15) and self.indicators.trend(self.prices,TrendPeriod) == 1):


			#if (self.indicators.trend(self.prices,TrendPeriod) == 1 and self.currentPrice > self.indicators.movingAverage(self.prices,10) and self.currentPrice > self.indicators.movingAverage(self.prices,20) and self.currentVolume > 2):
			#if (self.currentPrice < self.indicators.movingAverage(self.prices,20) and self.currentPrice < self.indicators.movingAverage(self.prices,60)):
			#if (self.indicators.trend(self.prices,TrendPeriod) == 1 and self.currentVolume > 20):

			if (self.indicators.movingAverage(self.prices,10) < self.indicators.movingAverage(self.prices,30) and self.indicators.trend(self.prices,TrendPeriod) == 1):
				self.trades.append(BotTrade(self.currentPrice))

		for trade in openTrades:

			if SL > 0:
				if (self.currentPrice < (float(trade.entryPrice) - float(SL))):
					trade.close(self.currentPrice)

			if TP > 0:
				if (self.currentPrice > (float(trade.entryPrice) - float(TP))):
					trade.close(self.currentPrice)

			#if (self.currentPrice > self.indicators.movingAverage(self.prices,15) and self.indicators.trend(self.prices,20) == 0):
			
			#if ((self.currentPrice > (float(trade.entryPrice) + float(TP))) or (self.currentPrice < (float(trade.entryPrice) - float(SL)))): # Take Proffit
			#if (self.indicators.movingAverage(self.prices,10) == self.indicators.movingAverage(self.prices,20)):

			#if (self.indicators.trend(self.prices,TrendPeriod) == 0):
			#if (self.indicators.trend(self.prices,TrendPeriod) == 0 and self.currentPrice < self.indicators.movingAverage(self.prices,10)and self.currentPrice < self.indicators.movingAverage(self.prices,20)):
			if (self.indicators.movingAverage(self.prices,10) > self.indicators.movingAverage(self.prices,30)):
				if (self.currentPrice > (float(trade.entryPrice))):
					trade.close(self.currentPrice)



	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()

"""
SubTotal: -1.66055751
TrendPeriod = 10
SL = 0.00001
SMA 10
SMA 30



"""


		