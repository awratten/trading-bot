from botlog import BotLog
from bcolors import bcolors
import time
from datetime import datetime

ar_pro = []
total = []
trade_end_time = []


class BotTrade(object):
	def __init__(self,currentPrice,stopLoss=0):
		self.output = BotLog()
		self.status = "OPEN"
		self.currentPrice = currentPrice
		self.entryPrice = currentPrice
		self.exitPrice = 0
		self.output.log("Trade opened")
		if (stopLoss):
			self.stopLoss = currentPrice - stopLoss
	
	def close(self,currentPrice):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		self.output.log("Trade closed")
		#trade_end_time.append(datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')) #
		#total.append(sum(ar_pro))


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
		trade_end_time.append(time.time())#(datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')) #
		total.append(sum(ar_pro))

	
	def export():

		filename = open("export.csv",'w')
		#for i in total:
		#	print('{:.20f}'.format(i[0]) + ',' + str(i[1]) ,file=filename)

		for i in range(len(trade_end_time)):
		    filename.write("{},{}\n".format(trade_end_time[i],total[i]))

		#filename.close()



			


'''		import csv

		with open("export.csv",'wb') as resultFile:
			wr = csv.writer(resultFile, dialect='excel')
			wr.writerow(ar_pro)
'''


'''		import csv
		RESULT = ['apple','cherry','orange','pineapple','strawberry']
		with open("output.csv",'wb') as resultFile:
    		wr = csv.writer(resultFile, dialect='excel')
    		wr.writerow(RESULT)'''