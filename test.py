from poloniex import Poloniex


class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.conn = Poloniex()

		self.pair = pair
		self.period = period

		self.startTime = 1491048000
		self.endTime = 1491591200

		#self.data = self.conn.api_query("returnChartPair",{"currentPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
		self.data = self.conn.returnChartData(self.pair, self.period, self.startTime, self.endTime)

	def getPoints(self):
		return self.data

print BotChart("poloniex" ,"BTC_XMR", 300).data[-2]
