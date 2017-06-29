from keras.models import load_model
from poloniex import Poloniex
from pandas import read_csv
import numpy

conn = Poloniex()
data = conn.returnChartData('BTC_ZEC', 300, 1498521600, 1498608000)

model = load_model('BTC_ZEC_10Days_5min_29_6_17.h5')
model.load_weights('BTC_ZEC_10Days_5min_29_6_17_weights.h5')

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)



dataframe = read_csv('btc_zec_1_day_5min.csv', usecols=[1], engine='python', skipfooter=3)
dataset = dataframe.values
dataset = dataset.astype('float32')


test = dataset#[train_size:len(dataset),:]

look_back = 1
testX, testY = create_dataset(test, look_back)
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))



def predict(data):
	prediction = model.predict(data)
	return prediction


#print(read_csv('btc_zec_10_days_5min.csv', usecols=[1], engine='python', skipfooter=3))
#print(testX)
print(model.predict(numpy.array([[ 0.1320001 ]])))