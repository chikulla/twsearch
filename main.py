#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twsearch import TweetSearch


def printtweets(tweets):
    for tweet in tweets:
        print(tweet.to_str())


def forever(search):
    while True:
        printtweets(search.next())


search = TweetSearch(u'吉村家')
forever(search)

