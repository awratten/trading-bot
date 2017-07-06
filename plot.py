from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot

def parser_clean(x):
	return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def parser(x):
	y = datetime.fromtimestamp(float(x))
	return (y.strftime('%d %H:%M:%S')) #datetime.fromtimestamp(float(x))#strptime(x, '%Y-%m-%d %H:%M:%S')


series = read_csv('export.csv', parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
series.plot()
pyplot.show()
