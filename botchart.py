from poloniex import Poloniex


class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.conn = Poloniex()

		self.pair = pair
		self.period = period

		self.startTime = 1496275200 #1497916800 #1496275200
		self.endTime = 1498000843  

		#self.data = self.conn.api_query("returnChartPair",{"currentPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
		self.data = self.conn.returnChartData(self.pair, self.period, self.startTime, self.endTime)

	def getPoints(self):
		return self.data
