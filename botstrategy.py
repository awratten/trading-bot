from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade



class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.opens = []
		self.closes = [] #for Momentum
		self.trades = []
		self.currentPrice = None
		self.numSimulTrades = 1
		self.stopLoss = 0.00001
		self.indicators = BotIndicators()

		self.trendPeriod = 3 # ETH : 3 # DASH : 3
		self.minVolume = 1.2 # ETH : 1.2 # DASH : 1


	def tick(self,candlestick):
		self.currentPrice = float(candlestick['weightedAverage'])
		self.currentVolume = float(candlestick['volume'])

		self.open = float(candlestick['open'])
		self.close = float(candlestick['close'])
		self.high = float(candlestick['high'])
		self.low = float(candlestick['low'])
		self.date = float(candlestick['date'])

		self.prices.append(self.currentPrice)
		self.closes.append(self.close) # for Momentum
		
		self.output.log("Price: "+str(candlestick['weightedAverage'])+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15))+"\tMomentum: "+str(self.indicators.momentum(self.closes))+"\tRSI: "+str(self.indicators.RSI(self.prices)))
		
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
			#print("Momentum: " + str(self.indicators.momentum(self.closes)))

			#print("Pivot: " + str(self.indicators.Pivot('BTC_ZEC', 300,self.date))) # dont need to calculate this every tick
			#print("RSI : " + str(self.indicators.RSI(self.prices)))

			if (self.indicators.trend(self.prices,self.trendPeriod) == 1 and self.currentVolume > self.minVolume):

			#if (self.indicators.RSI(self.prices,14) < 30 and self.currentVolume > self.minVolume):
					self.trades.append(BotTrade(self.currentPrice,stopLoss=self.stopLoss))

		for trade in openTrades:
			#if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
			if (self.indicators.trend(self.prices,self.trendPeriod) == 0 and self.currentVolume > self.minVolume):
			#if (self.indicators.RSI(self.prices,14) > 70 and self.currentVolume > self.minVolume):
					trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()

