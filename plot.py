import matplotlib.pyplot as plt
import csv

from numpy import genfromtxt
pr = genfromtxt('export.csv', delimiter=',')


plt.plot(pr)
plt.ylabel('profit')
plt.show()