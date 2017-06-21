from botlog import BotLog

ar_pro = []

class BotTrade(object):
	def __init__(self,currentPrice,stopLoss=0):
		self.output = BotLog()
		self.status = "OPEN"
		self.entryPrice = currentPrice
		self.exitPrice = 0
		self.output.log("Trade opened")
		if (stopLoss):
			self.stopLoss = currentPrice - stopLoss
	
	def close(self,currentPrice):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		self.output.log("Trade closed")

	def tick(self, currentPrice):
		if (self.stopLoss):
			if (currentPrice < self.stopLoss):
				self.close(currentPrice)


	def showTrade(self):
		tradeStatus = "Entry Price: "+str(self.entryPrice)+" Status: "+str(self.status)+" Exit Price: "+str(self.exitPrice)

		if (self.status == "CLOSED"):
			tradeStatus = tradeStatus + " Profit: "
			if (self.exitPrice > self.entryPrice):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"

			tradeStatus = tradeStatus+str(self.exitPrice - self.entryPrice)+"\033[0m"
			ar_pro.append(self.exitPrice - self.entryPrice)

		self.output.log(tradeStatus)
		self.output.log("SubTotal: " + str((sum(ar_pro))))
	
