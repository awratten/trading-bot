from poloniex import Poloniex
import time, datetime

csvfile = open("btc_zec_10_days_5min.csv", "a")


conn = Poloniex()

security = 'BTC_ZEC'
period = 300
#Days = 230
Days = 10

startTime = time.time() - (86400 * Days)
endTime = time.time() #End at current time

data = conn.returnChartData(security, period, startTime, endTime)

def datetime_from_timestamp(timestamp):
	x = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	return x


for tick in data:
	print(str(datetime_from_timestamp(tick['date'])) + "," + tick['close'], file=csvfile)

