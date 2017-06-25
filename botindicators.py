from poloniex import Poloniex
from datetime import datetime, date, time, timedelta

Pivot_date = 0
curPivot = 0

class BotIndicators(object):
	def __init__(self):
		pass

	def movingAverage(self, dataPoints, period):
		if (len(dataPoints) > 0):
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

	def momentum (self, dataPoints, period=14):
		"""https://www.mql5.com/en/code/7781"""
		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	
	def Pivot(self, pair, period, cdate):
		global Pivot_date, curPivot
		curDay = datetime.combine(datetime.fromtimestamp(cdate), time(0, 0, 0))

		if curDay == Pivot_date:
			return curPivot
		else:
			polo = Poloniex()
		
			#dt = datetime.combine(date.today(), time(0, 0, 0)) # get start of today
			dt = datetime.combine(datetime.fromtimestamp(cdate), time(0, 0, 0)) # get start of today

			Pivot_date = dt
			
			startTime = int((dt - timedelta(days=1)).timestamp()) 
			endTime = int((dt - timedelta(seconds=1)).timestamp())
			
			data = polo.returnChartData(pair, period, startTime, endTime)

			highs = []
			lows = []
			closes = []

			for i in data:
				highs.append(float(i['high']))
				lows.append(float(i['low']))
				closes.append(float(i['close']))

			avHigh = sum(highs) / len(highs)
			avLow = sum(lows) / len(lows)
			avClose = sum(closes) / len(closes)

			PP = (float(avHigh) + float(avLow) + float(avClose)) / 3
			curPivot = PP
			return PP





