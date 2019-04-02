from nltk import pos_tag
from nltk.tokenize import word_tokenize


def check(word1_tag,word2_tag,word3_tag):

	if((word1_tag=="JJ") and ((word2_tag=="NN") or (word2_tag=="NNS"))):
		return 1
	elif((word1_tag=="JJ") and (word2_tag=="JJ")):
		if((word3_tag!="NN") and (word3_tag!="NNS")):
			return 2
		return 0
	elif(((word1_tag=="NN")or (word1_tag=="NNS")) and (word2_tag=="JJ")):
		if(word3_tag!="NN" or word3_tag!="NNS"):
                        return 3
		else:
			return 0
	elif((word1_tag=="RB" or word1_tag=="RBR" or word1_tag=="RBS") and (word2_tag=="JJ")):
		if(word3_tag!="NN" and word3_tag!="NNS"):
                        return 4
		else:
			return 0
	elif(((word1_tag=="RB") or (word1_tag=="RBR") or (word1_tag=="RBS")) and ((word2_tag=="VB") or (word2_tag=="VBD") or (word2_tag=="VBN") or (word2_tag=="VBG"))):
		return 5
	else:
		return 0
	return 0



def calculate_sentiment(pattern):
	print("Pattern - Length :: ",len(pattern))
	sentiment=0
	#print(pattern)
	k_word=pattern[0].split(" ")
	print(k_word[0],"-------",k_word[1])
	with open("afinn-2047.txt") as afinn:
		for line in afinn:
			word=line.split(" ")
			if k_word[0] in word:
				sentiment=sentiment+int(word[1])
				print("found1")
			if k_word[1] in word:
				sentiment=sentiment+int(word[1])
				print("found2")

	print("Sentiment",sentiment)
	return sentiment


def decide_polarity(sentiment):
	if sentiment > 0:
		return 1
	elif sentiment <0:
		return -1
	else:
		return 0


def get_sentiment(tweet,total):
	return tweet*100/total


def get_verdict(sentiment):
	maximum=max(sentiment)
	index=sentiment.index(maximum)

	if(index==0):
		verdict="positive"
	elif(index==1):
		verdict="neutral"
	else:
		verdict="negative"

	return verdict


def format_output(positive_tweet,neutral_tweet,negative_tweet):
	total_tweets=positive_tweet+neutral_tweet+negative_tweet
#	output={'positive':positive_tweet/total_tweet,
#		'neutral':neutral_tweet/total_tweet,
#		'negative':negative_tweet/total_tweet}
#	return output
	output=[]
	sentiments=[]
	positive_sentiment=get_sentiment(positive_tweet,total_tweets)
	negative_sentiment=get_sentiment(negative_tweet,total_tweets)
	neutral_sentiment=get_sentiment(neutral_tweet,total_tweets)
	sentiments.append(positive_sentiment)
	sentiments.append(neutral_sentiment)
	sentiments.append(negative_sentiment)
	output.append("Postive"+": "+str(positive_sentiment)+"%")
	output.append("Neutral"+": "+str(neutral_sentiment)+"%")
	output.append("Negative"+": "+str(negative_sentiment)+"%")
	verdict=get_verdict(sentiments)
	output.append("Final Verdict is "+": "+verdict)
	return output


def classifier():
	
	with open("calculate_polarity.txt","r") as txt:
		neutral_tweet=0
		positive_tweet=0
		negative_tweet=0
		for x in txt:
			print(x)
			tokens=word_tokenize(x)
			taggeddata=pos_tag(tokens)
			print(taggeddata)
			pattern=[]
			sentiment=0
			for k in range(len(taggeddata)-2):

				value=check(taggeddata[k][1],taggeddata[k+1][1],taggeddata[k+2][1])
				if(value>0):
					pattern=[]
					pattern.append("".join(taggeddata[k][0])+" "+"".join(taggeddata[k+1][0]))
					pattern.append("\n")
					sentiment=sentiment+calculate_sentiment(pattern)
					print(pattern)
			print("Sentiment",sentiment)
			polarity=decide_polarity(sentiment)
			print(polarity)
			if  (polarity==0):
				neutral_tweet+=1
			elif (polarity > 0):
				positive_tweet+=1
			else:
				negative_tweet+=1

		output=format_output(positive_tweet,neutral_tweet,negative_tweet)
		print(output)
		print("+ve ::",positive_tweet,"\n","-ve ::",negative_tweet,"\n","0 ::",neutral_tweet)
		
		return output
