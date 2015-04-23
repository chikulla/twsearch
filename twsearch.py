#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import json

import requests
from bs4 import BeautifulSoup

from tw import Tweet


class TweetSearch:
    def __init__(self, query):
        self.query = str(urllib.parse.quote(query.encode('utf-8')))
        self.cursor = ""

    def next(self):
        if self.cursor == "":
            url = "https://twitter.com/search?f=realtime&q=" + \
                  self.query + "&src=typd&lang=ja"
            resp = requests.get(url)
            self.soup = BeautifulSoup(resp.text.encode(resp.encoding))
            self.encoding = resp.encoding
            self.init = False
            self.cursor = self.findattrval("data-scroll-cursor", self.soup);
        else:
            url = "https://twitter.com/i/search/timeline?q=" + self.query + \
                  "&include_available_features=1" \
                  "&include_entities=1&scroll_cursor=" + self.cursor
            resp = requests.get(url)
            jsonhtml = json.loads(resp.text)
            self.cursor = jsonhtml["scroll_cursor"]
            self.soup = BeautifulSoup(jsonhtml["items_html"])
        return self.parsetweets()

    def findattrval(self, attrkey, soup):
        results = soup.find_all(attrs={attrkey: True})
        if len(results):
            return results[0][attrkey]
        return ""

    def parsetweet(self, soup):
        tweetid = self.findattrval("data-tweet-id", soup)
        screenname = self.findattrval("data-screen-name", soup)
        name = self.findattrval("data-name", soup)
        timestamp = self.findattrval("data-time", soup)
        message = soup.find_all(class_="tweet-text")
        if len(message):
            message = message[0].text
        else:
            message = ""
        return Tweet(tweetid, screenname, name, timestamp, message)

    def parsetweets(self):
        result = []
        tweets = self.soup.find_all(attrs={"data-item-type": "tweet"})
        for tweet in tweets:
            result.append(self.parsetweet(tweet))
        return result

