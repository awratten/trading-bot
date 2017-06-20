class BotIndicators(object):
	def __init__(self):
		pass

	def movingAverage(self, dataPoints, period):
		if (len(dataPoints) > period):
			return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))

	def trend (self, dataPoints, period):
		if (len(dataPoints) > period):
			prev_period = 2 * period
			cur = sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
			prev = sum(dataPoints[-prev_period:-period]) / float(len(dataPoints[-prev_period:-period]))
			if (cur > prev):
				return 1
			else:
				return 0