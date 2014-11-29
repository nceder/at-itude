#!/usr/bin/env python

""" Gathers data from twitter based on keyword list and geoposition

    nrc 29/11/2014

"""

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import os

import json
from collections import Counter

from postcodes import PostCoder

# keys from twitter dev program needed
consumer_key=os.environ['CONSUMER_KEY']
consumer_secret=os.environ['CONSUMER_SECRET_KEY']

access_token=os.environ['ACCESS_TOKEN']
access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]

api = tweepy.API(auth)
word_list = ['gay', 'lesbian', 'bi', 'trans']

word_cnt = Counter(word_list)

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        json_data = json.loads(data)
        if 'text' not in json_data:
            return True
        if json_data['text'].startswith("RT"):
            return True
        for word in word_list:
            if word.lower() in json_data['text'].lower():
                word_cnt[word] += 1 
        print json_data['text'], word_cnt.most_common(3)
        
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    lat, long, place = get_geo(sys.argv[1])

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    try:
        stream.filter(track=word_list, locations=[long-0.5, lat-0.5,long+0.5, lat+0.5])
    except KeyboardInterrupt:
        print "\n\nThe folks in %s are:" % place
    
        for w, c in word_cnt.most_common(10):
            print w, c


