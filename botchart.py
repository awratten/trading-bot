from poloniex import Poloniex


class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.conn = Poloniex("N9GVZF8Y-WGYIMIXP-UNKOUYKA-E914X4YB","8047b4808f013cceadf52f25253ca1b618216bf7d6bff84d79274eac10cf1985260d51fd9f1ffae333f752695c6b2985b7a9da6a4462e97a82879a0365a98dda")

		self.pair = pair
		self.period = period

		self.startTime = 1483228800 #1491048000
		self.endTime = 1497968441 #1491591200

		#self.data = self.conn.api_query("returnChartPair",{"currentPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
		self.data = self.conn.returnChartData(self.pair, self.period, self.startTime, self.endTime)

	def getPoints(self):
		return self.data
