from poloniex import Poloniex
import time

class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.conn = Poloniex()

		self.pair = pair
		self.period = period
		
		Days = 10			#TODO: Fix Naming of this variable


		self.startTime = 1499309550 - (86400 * Days)
		self.endTime = 1499309550

		#self.startTime = time.time() - (86400 * Days)
		#self.endTime = time.time() #End at current time

		
		self.data = self.conn.returnChartData(self.pair, self.period, self.startTime, self.endTime)
		#self.data = self.conn.returnTicker()[self.pair]


	def getPoints(self):
		return self.data

