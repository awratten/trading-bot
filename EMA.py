from poloniex import Poloniex #https://github.com/s4w3d0ff/python-poloniex
import time
import numpy as np

conn = Poloniex()

pair = 'BTC_ZEC'
period = 300
		
Days = 1			#TODO: Fix Naming of this variable

startTime = time.time() - (86400 * Days)
endTime = time.time() #End at current time


data = conn.returnChartData(pair, period, startTime, endTime)

prices = []

def movingAverage(dataPoints, period):
	if (len(dataPoints) > 0):
		return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))


def SMA(dataPoints, period):
	if len(dataPoints) < period:
		return None
	return sum(dataPoints[-period:]) / float(period)


def EMA(dataPoints, period=14, position=None, previous_ema=None):
	"""https://www.oanda.com/forex-trading/learn/forex-indicators/exponential-moving-average"""
	#print(dataPoints)
	if (len(dataPoints) < period + 2):
		return None
	c = 2 / float(period + 1)
	if not previous_ema:
		return EMA(dataPoints, period, period, movingAverage(dataPoints[-period*2 + 1:-period + 1], period))
	else:
		current_ema = (c * dataPoints[-position]) + ((1 - c) * previous_ema)
		if (position > 0):
			return EMA(dataPoints, period, position - 1, current_ema)
	return previous_ema


def MACD(dataPoints, nslow=26, nfast=12):
	"""
	compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
	return value is emaslow, emafast, macd which are len(dataPoints) arrays
	"""
	emaslow = EMA(dataPoints, nslow)
	emafast = EMA(dataPoints, nfast)
	if(emafast == None and emaslow == None):
		return None, None, None
	else:
		return emaslow, emafast, emafast - emaslow



for i in data:
	close = float(i['close'])
	prices.append(close)


#print(prices)
print(movingAverage(prices, 14))
print(SMA(prices, 14))
print(EMA(prices,14))
print(MACD(prices))



'''
    Exponential Moving Average (EMA)
    Exponentially smoothed moving average is calculated by adding the moving average of a certain share of the current closing price to the previous value. With exponentially smoothed moving averages, the latest prices are of more value. P-percent exponential moving average will look like:

    EMA = (CLOSE(i)*P)+(EMA(i-1)*(100-P))

    Where:
	CLOSE(i) — the price of the current period closure;
	EMA(i-1) — Exponentially Moving Average of the previous period closure;
	P — the percentage of using the price value.
'''