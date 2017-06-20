from botlog import BotLog

ar_pro = []

class BotTrade(object):
	def __init__(self, currentPrice):
		self.output = BotLog()
		self.status = "OPEN"
		self.entryPrice = currentPrice
		self.exitPrice = 0
		self.output.log("Trade opened")

	def close(self,currentPrice):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		self.output.log("Trade Closed")

	def showTrade(self):
		
		tradeStatus = "Entry Price: "+str(self.entryPrice)+" Status: "+str(self.status)+" Exit Price: "+str(self.exitPrice)

		if (self.status == "CLOSED"):
			tradeStatus = tradeStatus + " Profit: "
			if (self.exitPrice > self.entryPrice):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"

		print (self.exitPrice)
		
		tradeStatus = tradeStatus+str(self.exitPrice - self.entryPrice) + "\033[0m"
		
		ar_pro.append(self.exitPrice - self.entryPrice)
		totalProffit = sum(ar_pro)

		self.output.log(tradeStatus)
		self.output.log("SubTotal: " + str(totalProffit))