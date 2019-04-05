#!/usr/bin/python3

# check file exist
import os
# listen to the tweets
from tweepy.streaming import StreamListener
# auth the twitter account
from tweepy import OAuthHandler
from tweepy import Stream
# import creadentials
import twitterCredentials
# restrict amount of time extraction will be done for
import time
# format json for processing
#from formatJSON import formatJSON
import json

# for checking input
import re
# stub
#from stub import TweepyStub

from sentiment_analysis import *

# class to filter the input list


class Filter():
    def __init__(self, list):
        self.list = list

    def filter(self):
        flag = 0
        for i in range(len(self.list)):
            valid_st = re.sub(r'[^0-9a-zA-Z]', '', self.list[i])
            if(len(valid_st) == 0):
                flag = 1
            if(len(valid_st) == 1):
                flag = 1

        if(flag == 1):
            print("Invalid input!")
            return False
        if(flag == 0):
            print("Valid input!")
            return True


# class to format extracted unstructured json

class formatJSON():
    def __init__(self, fileName):
        self.fileName = fileName

    def formatJSON(self):
        path = "structTweets.json"
        if os.path.exists(path):
            os.remove(path)
            print("struct file deleted")
        newJSON = open(path, 'w')
        newJSON.write('[ ')
        with open(self.fileName, 'r') as infile:
            data = infile.read()
            new_data = data.replace('}\n{', '},\n{')
            json_data = json.loads(f'[{new_data}]')
            print(json_data)
            newJSON.write(new_data)
        newJSON.write(' ]')
        newJSON.close()


# class to stream tweets and stores it into a file


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    # stream_tweets method takes filename and keywords as an argument

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the twitter streaming API.
        listener = StdOutListener(fetched_tweets_filename)
        # OAuthHandler class from tweepy
        auth = OAuthHandler(twitterCredentials.CONSUMER_KEY,
                            twitterCredentials.CONSUMER_SECRET)
        # to complete authentication
        auth.set_access_token(twitterCredentials.ACCESS_TOKEN,
                              twitterCredentials.ACCESS_TOKEN_SECRET)
        # create twitter stream from class Stream we imported
        # listener object deals with tweets and error
        stream = Stream(auth, listener, tweet_mode='extended')
        # filter the tweets based on keywords using stream class filter method
        # feed track list with keywords
        stream.filter(languages=["en"], track=hash_tag_list)


# Inheret from StreamListener class.
class StdOutListener(StreamListener):
    """
    This is a basic listener class that just print received tweets
    to stdout.
    """

    # constructor

    def __init__(self, fetched_tweets_filename, timeLimit=20):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.startTime = time.time()
        self.limit = timeLimit

    # StreamListener method which can be overridden
    # take data from stream listner

    def on_data(self, data):
        try:
            print(data)  # print data we got.
            if (time.time() - self.startTime) < self.limit:
                with open(self.fetched_tweets_filename, 'a') as tf:
                    if (time.time() - self.startTime) < self.limit:
                        tf.write(data)
                        return True
                    else:
                        tf.close()
                        return False
            else:
                print("Nothing retrived")
                return False
        except BaseException as e:
            # print error and exception
            print("Error on data: %s" % str(e))

    # method from StreamListener, invoke on error

    def on_error(self, status):
        print(status)
        raise Exception('Some error occured.')


class AutomateAll(StdOutListener, formatJSON):
    def __init__(self, keywordList):
        self.keywordList = keywordList

    def extractStructTweets(self):
        try:
            filter = Filter(self.keywordList)
            if not filter.filter():
                list = ['Invalid input. Try again.', '']
                return list
            unStructFile = "UnstructTweets.json"
            if os.path.exists(unStructFile):
                os.remove(unStructFile)
                print("unstruct file deleted")
            twitterStreamer = TwitterStreamer()
            print("twitter streamer start")
            twitterStreamer.stream_tweets(unStructFile, self.keywordList)
            print("twitter streamer done")
            if os.stat(unStructFile).st_size == 0:
                # file is empty
                list = [
                    'Not enough people are tweeting on this topic. Please try again later.', '']
                return list
            format = formatJSON(unStructFile)
            format.formatJSON()
            # Vivek's function
            customer = sentiment_Analysis()
            return customer.getResult()
        except Exception as e:
            print(e)
            list = ['Oops, twitter blocked our request, please try again later.', '']
            return list


class API(StdOutListener, formatJSON):
    def __init__(self, keywordList):
        self.keywordList = keywordList

    def toJSON(self, list):
        # convert list to dictionary and then json
        if len(list) == 4:
            x = {
                'analysis':
                    {
                        'positive': list[0],
                        'neutral': list[1],
                        'negative': list[2],
                        'verdict': list[3]
                    }
            }
            # x = {}
            # x["positive"] = list[0]
            # x["neutral"] = list[1]
            # x["negative"] = list[2]
            # x["verdict"] = list[3]
        else:
            x = {
                'error':
                    {
                        list[0]
                    }
            }

        print("Json dumps print")
        print(json.dumps(x))
        print(type(x))
        print(type(json.dumps(x)))
        # return json.dumps(x)
        return x

    def jsonAnalysis(self):
        try:
            filter = Filter(self.keywordList)
            if not filter.filter():
                list = ['Invalid input. Try again.']
                return self.toJSON(list)
            unStructFile = "UnstructTweets.json"
            if os.path.exists(unStructFile):
                os.remove(unStructFile)
                print("unstruct file deleted")
            twitterStreamer = TwitterStreamer()
            print("twitter streamer start")
            print("keywords: ")
            print(self.keywordList)
            twitterStreamer.stream_tweets(unStructFile, self.keywordList)
            print("twitter streamer done")
            if os.stat(unStructFile).st_size == 0:
                # file is empty
                list = [
                    'Not enough people are tweeting on this topic. Please try again later.']
                return self.toJSON(list)
            format = formatJSON(unStructFile)
            format.formatJSON()
            # Vivek's function
            customer = sentiment_Analysis()
            return self.toJSON(customer.getResult())
        except Exception as e:
            print(e)
            list = ['Oops, twitter blocked our request, please try again later.']
            return self.toJSON(list)


if __name__ == "__main__":
    hash_tag_list = ['narendra modi', 'amit shah', 'yogi adityanath']
    fetched_tweets_filename = "UnstructTweets.json"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

# format the saved tweets
    # tweetSaveFile = "UnstructTweets.json"
    # formatJSON = formatJSON(tweetSaveFile)
    # formatJSON.formatJSON()
