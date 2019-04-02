import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

#Tokenizing is done here 



def get_modify(sentence):
	tokens=word_tokenize(sentence.lower())
#	print(tokens)
	modified_sentence=""
	for w in tokens:
		if w not in stopwords.words('english'):
			modified_sentence=modified_sentence+" "+w

	return modified_sentence.lower()



def preprocess():
	with open("Tweets_extracted.txt","r") as file:
		output_file=open("calculate_polarity.txt","w+")
		count=0
		for sentence in file:
			sentence=re.sub(r"[^a-zA-Z0-9]+",' ',sentence)
#			sentence=re.sub("[.@#]+",' ',sentence)
			modified_sentence=get_modify(sentence)

			print(modified_sentence)
			output_file.write(modified_sentence)
			output_file.write("\n")
			count=count+1
		print(count)
		output_file.close()



#preprocess()
