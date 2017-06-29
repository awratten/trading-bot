def datetime_from_timestamp(timestamp):
	x = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	return x


def WriteData2csv(filename, pair='BTC_ZEC', period=300, days=230):
	from poloniex import Poloniex
	import time, datetime

	csvfile = open(filename, "a")
	conn = Poloniex()

	startTime = time.time() - (86400 * days)
	endTime = time.time() #End at current time

	data = conn.returnChartData(pair, period, startTime, endTime)


	for tick in data:
		#print(str(datetime_from_timestamp(tick['date'])) + "," + tick['close'], file=csvfile)
		print(tick['close'], file=filename)


