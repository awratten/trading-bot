from poloniex import Poloniex


class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.conn = Poloniex('79GA9FNK-4UQ9665O-LQQJ2CT4-57Y378P5','c6c34ee11cd0cb65b0fb1930974f6bbb1adde2052c2e9cd225de7f4408f9d228e4a2ad9c057601e6626eb83576c6b08fa43c9e034d9b72ca037dd74a1801bb16')

		self.pair = pair
		self.period = period

		self.startTime = 1491048000
		self.endTime = 1491591200

		#self.data = self.conn.api_query("returnChartPair",{"currentPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
		self.data = self.conn.returnChartData(self.pair, self.period, self.startTime, self.endTime)

	def getPoints(self):
		return self.data

#print (BotChart("poloniex" ,"BTC_XMR", 300).data[-2])

polo = Poloniex('79GA9FNK-4UQ9665O-LQQJ2CT4-57Y378P5','c6c34ee11cd0cb65b0fb1930974f6bbb1adde2052c2e9cd225de7f4408f9d228e4a2ad9c057601e6626eb83576c6b08fa43c9e034d9b72ca037dd74a1801bb16')

print(polo.returnBalances())