import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

#[300, 900, 1800, 7200, 14400, 86400]:


def main(argv):
	chart = BotChart("poloniex", "BTC_ETH", 7200)

	strategy = BotStrategy()

	for candlestick in chart.getPoints():
		if candlestick != "error":
			strategy.tick(candlestick)
		else:
			print 'error'

if __name__ == "__main__":
	main(sys.argv[1:])
