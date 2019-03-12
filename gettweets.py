#!/usr/bin/python3

# listen to the tweets
from tweepy.streaming import StreamListener
# auth the twitter account
from tweepy import OAuthHandler
from tweepy import Stream
# import creadentials
import twitterCredentials


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
        stream = Stream(auth, listener)
        # filter the tweets based on keywords using stream class filter method
        # feed track list with keywords
        stream.filter(track=hash_tag_list)


# Inheret from StreamListener class.
class StdOutListener(StreamListener):
    """
    This is a basic listener class that just print received tweets
    to stdout.
    """

    # constructor

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # StreamListener method which can be overridden
    # take data from stream listner

    def on_data(self, data):
        try:
            print(data)  # print data we got.
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            # print error and exception
            print("Error on data: %s" % str(e))

    # method from StreamListener, invoke on error
    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    hash_tag_list = ['narendra modi', 'rahul gandhi', 'yogi adityanath']
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
