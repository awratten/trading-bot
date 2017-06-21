from poloniex import Poloniex
import time

class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.conn = Poloniex()

		self.pair = pair
		self.period = period
		
		Days = 1			#TODO: Fix Naming of this variable

		self.startTime = time.time() - (86400 * Days)
		self.endTime = time.time()  #End at current time

		#self.data = self.conn.api_query("returnChartPair",{"currentPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
		self.data = self.conn.returnChartData(self.pair, self.period, self.startTime, self.endTime)

	def getPoints(self):
		return self.data
