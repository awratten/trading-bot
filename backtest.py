import sys, getopt
import datetime, time

from botchart import BotChart
from botstrategy import BotStrategy

#[300, 900, 1800, 7200, 14400, 86400]:

def main(argv):
	#chart = BotChart("poloniex", "BTC_ETH", 300)
	chart = BotChart("poloniex", "BTC_ZEC", 300)
	#chart = BotChart("poloniex", "BTC_DASH", 300)

	strategy = BotStrategy()

	for candlestick in chart.getPoints():
		#print(candlestick)
		strategy.tick(candlestick)


if __name__ == "__main__":
	main(sys.argv[1:])




"""
ZEC 300 trent(5) and Vol > 1 on both open and close trade

1 Day Test = +0.69697851 / 0.7032790300000004
2 Day Test = +0.0370762400000125 / 0.1876898000000317
3 Day Test = -3.8008370200000097
3 Day Test = -2.4596537600000663 with Volume > 1
3 Day Test = -2.8192105399998577 with Volume > 2
3 Day Test = -3.9808894799998993 with Volume > 0.75
3 Day Test = -2.312605410000159 with Volume > 1 open and close
4 Day Test = +0.7931198299999244 / 2.3524328099998004
7 Day Test = +61.565436730012834 / 63.15507843000876


ZEC 300 | Trend(5) | vol > 1.1
1 Day : 1.0202646200000092 
2 Day : 0.5085170100000375
3 Day : -1.7376553799999654 **********
4 Day : 2.680906879999767
7 Day : 62.9819900200051

ZEC 300 | Trend(3) | vol > 1.2
1 Day : 1.7265721400000251
2 Day : 2.1683305500000354
3 Day : 0.32830000999981457
4 Day : -2.812878100000112
7 Day : 109.6339515900101



ETH 300 | Trend(5) | vol > 1.1
1 Day : 0.3715683700000022
2 Day : -0.484927010000027
3 Day : -1.1133912300001152
4 Day : -0.9789515200000011
7 Day : 3.3798927999969717
"""

