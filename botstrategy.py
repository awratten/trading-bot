from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

from bcolors import bcolors



class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.opens = []
		self.closes = [] #for Momentum
		self.trades = []
		
		self.MACD_History = [] # MACD History
		self.MACD_Signal_History = [] # MACD Signal History

		self.currentPrice = None
		self.numSimulTrades = 1
		self.takeProfit = 0.0001
		self.stopLoss = 1
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
		
		self.output.log("Price: " + str(candlestick['weightedAverage'])+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15))+"\tMomentum: "+str(self.indicators.momentum(self.closes))+"\tRSI: "+str(self.indicators.RSI(self.prices)))
		
		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()


	def evaluatePositions(self):
		MacdCurrent = None
		MacdPrevious = None
		SignalCurrent = None
		SignalPrevious = None


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

			#slow, fast, signal = self.indicators.MACD(self.closes)
			#print(slow)
			#print(fast)
			#print(signal)


			
			if (len(self.closes) > 26 + 2): # Need to have enought prices in order to calculate the slowEMA
				SlowEMA = (self.indicators.EMA(self.closes, 26))
				FastEMA = (self.indicators.EMA(self.closes, 12))

				self.MACD_History.append(self.indicators.iMACD(SlowEMA,FastEMA))
				
				MacdCurrent = self.MACD_History[-1] # this is the most recent MACD in the list
				
				if (len(self.MACD_History) > 2):
					MacdPrevious = (self.MACD_History[-2]) # This is the second most recent MACD in the List
				
				if (len(self.MACD_History) > 9 + 2):
					SignalCurrent = self.indicators.EMA(self.MACD_History,9) 
					self.MACD_Signal_History.append(SignalCurrent)
				
					if (len(self.MACD_Signal_History) > 2):
						SignalPrevious = self.MACD_Signal_History[-2]
						#print("MACD: ")
						#print(MacdCurrent)
						#print(MacdPrevious)
						#print(SignalCurrent)
						#print(SignalPrevious)


			if (len(self.closes) > 100):
				if (MacdCurrent and MacdPrevious and SignalCurrent and SignalPrevious):
					if (MacdCurrent < 0 and MacdCurrent > SignalCurrent and MacdPrevious < SignalPrevious and self.indicators.RSI(self.prices,14) < 50):	 
						self.trades.append(BotTrade(self.currentPrice,stopLoss=self.stopLoss))


			#if (self.indicators.trend(self.prices,self.trendPeriod) == 1 and self.currentVolume > self.minVolume):
				#self.trades.append(BotTrade(self.currentPrice,stopLoss=self.stopLoss))
			#if (self.indicators.RSI(self.prices,14) < 30 and self.currentVolume > self.minVolume):
			#		self.trades.append(BotTrade(self.currentPrice,stopLoss=self.stopLoss))

		#print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC
		
		for trade in openTrades:

			currentProfit = float(self.currentPrice) - float(trade.entryPrice)
			if currentProfit > 0:
				print("entry: " + str(trade.entryPrice))
				print(bcolors.OKGREEN + str(currentProfit) + bcolors.ENDC)
			else:
				print("entry: " + str(trade.entryPrice))
				print(bcolors.WARNING + str(currentProfit) + bcolors.ENDC)

			#if (MacdCurrent and MacdPrevious and SignalCurrent and SignalPrevious):
			#	if (MacdCurrent > 0 and MacdCurrent < SignalCurrent and MacdPrevious > SignalPrevious):
			
			if (self.currentPrice >= (float(trade.entryPrice) + self.takeProfit) or self.date > 1499309550 - 300):
					trade.close(self.currentPrice)



			#if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
			#if (self.indicators.trend(self.prices,self.trendPeriod) == 0 and self.currentVolume > self.minVolume):
			#if (self.indicators.RSI(self.prices,14) > 70 and self.currentVolume > self.minVolume):
			#		trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()



#3.9229976200001926
#3.9229976200001926

"""

   MacdCurrent=iMACD(NULL,0,12,26,9,PRICE_CLOSE,MODE_MAIN,0);
   MacdPrevious=iMACD(NULL,0,12,26,9,PRICE_CLOSE,MODE_MAIN,1);
   SignalCurrent=iMACD(NULL,0,12,26,9,PRICE_CLOSE,MODE_SIGNAL,0);
   SignalPrevious=iMACD(NULL,0,12,26,9,PRICE_CLOSE,MODE_SIGNAL,1);
   MaCurrent=iMA(NULL,0,MATrendPeriod,0,MODE_EMA,PRICE_CLOSE,0);
   MaPrevious=iMA(NULL,0,MATrendPeriod,0,MODE_EMA,PRICE_CLOSE,1);

if (MacdCurrent<0 && MacdCurrent>SignalCurrent && MacdPrevious<SignalPrevious)
       if (MathAbs(MacdCurrent)>(MACDOpenLevel*sdPoint) && MaCurrent>MaPrevious)
        if (TradingHours() == true)
         {
          if (ECN.Broker == false) ticket=OrderSend(Symbol(),OP_BUY,Lots,Ask,RealSlippage,Ask-StopLossLong*sdPoint,Ask+TakeProfitLong*sdPoint,YourOrderComment,MagicNumber,0,Green);
          else
            {
              ticket=OrderSend(Symbol(),OP_BUY,Lots,Ask,RealSlippage,0,0,YourOrderComment,MagicNumber,0,Green); // Send order without stops
           
              if (ticket > -1) AddLiteralStopsByPips(ticket, OP_BUY, StopLossLong, TakeProfitLong); 
           
            }        
 
          return(0); 
         }


#// should it be closed?
                     if (MacdCurrent>0 && MacdCurrent<SignalCurrent && MacdPrevious>SignalPrevious)
                       if (MacdCurrent>(MACDCloseLevel*sdPoint))
                         {
                          OrderClose(OrderTicket(),OrderLots(),Bid,RealSlippage,Violet); // close position
                          return(0); // exit

"""