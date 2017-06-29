from poloniex import Poloniex
from datetime import datetime, date, time, timedelta

import numpy as np

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


		

	def RSI(self, prices, period=14):
		deltas = np.diff(prices)
		seed = deltas[:period+1]
		up = seed[seed >= 0].sum()/period
		down = -seed[seed < 0].sum()/period
		rs = up/down
		rsi = np.zeros_like(prices)
		rsi[:period] = 100. - 100./(1. + rs)

		for i in range(period, len(prices)):
			delta = deltas[i - 1]  # cause the diff is 1 shorter

			if delta > 0:
				upval = delta
				downval = 0.
			else:
				upval = 0.
				downval = -delta

			up = (up*(period - 1) + upval)/period
			down = (down*(period - 1) + downval)/period

			rs = up/down
			rsi[i] = 100. - 100./(1. + rs)

		if len(prices) > period:
			return rsi[-1]
		else:
			return 50 # output a neutral amount until enough prices in list



	def moving_average(self, dataPoints, period, type='simple'):
		dataPoints = np.asarray(dataPoints)
		if type == 'simple':
			weights = np.ones(period)
		else:
			weights = np.exp(np.linspace(-1., 0., period))

		weights /= weights.sum()

		a = np.convolve(dataPoints, weights, mode='full')[:len(dataPoints)]
		a[:period] = a[period]

		return a

	def MACD(self, dataPoints, nslow=26, nfast=12):
		"""
		compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
		return value is emaslow, emafast, macd which are len(dataPoints) arrays
		"""
		emaslow = moving_average(dataPoints, nslow, type='exponential')
		emafast = moving_average(dataPoints, nfast, type='exponential')
		return emaslow, emafast, emafast - emaslow