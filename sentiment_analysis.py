from extract import *
from classifier import *
from preprocess import *

class sentiment_Analysis:
	
	def getResult(self):
		dataextraction()
		preprocess()
		result=classifier()
		return result

