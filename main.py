#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import json
import string
import random
from google.appengine.ext import ndb
import time
import sys
import tweepy
import twittercreds

reload(sys)
sys.setdefaultencoding('utf-8')

# project files
import getTweets
import parseTweets
import tweetModel


def generateSecret():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))


class Secret(ndb.Model):
    """data base for secrets"""
    secretString = ndb.StringProperty(required=True)
    timeAdded = ndb.StringProperty(required=True)


class SecretHandler(webapp2.RequestHandler):
    """Responsible for handing out secrets and adding them to the database.
	Secrets are to be purged every 10 minutes from the database IF they are
	are secrets in the database"""

    def get(self):
        # make a json with the secret and add it to the database of secrets
        newSecret = Secret(secretString=generateSecret(), timeAdded=time.asctime(time.localtime(time.time())))
        newSecret.put()

        self.response.write(json.dumps(newSecret.to_dict()))

def getUserProfilePic(username):
    auth = tweepy.OAuthHandler(twittercreds.consumerKey, twittercreds.consumerSecret)
    auth.set_access_token(twittercreds.accessToken, twittercreds.accessTokenSecret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    userData = api.get_user(username)
    return userData['profile_image_url_https']

class TweetMaker(webapp2.RequestHandler):

    def get(self, username=None):
        if username:
            userProfilePic = getUserProfilePic(username)
            theTweets = getTweets.Tweets(username)
            theTweets.getLotsOfTweets()
            # tweet parser and formatter
            tweetsFormatted = parseTweets.TweetsParser()
            # generate tweets from corus
            makeTweets = tweetModel.DotardTweets()

            theTweets.newTweetData = tweetsFormatted.formatTweets(theTweets.newTweetData)
            makeTweets.makeModelFromList(theTweets.newTweetData)

            tweets = makeTweets.generateTweetsFromModel(20)
            # test if this is the problem
            finalTweets = {'username': username, 'userProfilePic': userProfilePic, 'theTweets': tweets}
            self.response.write(json.dumps(finalTweets))
        else:
            self.response.write('error')




    def post(self):
        requestData = json.loads(self.request.body)
        userData = requestData['username']
        # print userData
        theTweets = getTweets.Tweets(userData)
        theTweets.getLotsOfTweets()
        # tweet parser and formatter
        tweetsFormatted = parseTweets.TweetsParser()
        # generate tweets from corus
        makeTweets = tweetModel.DotardTweets()

        theTweets.newTweetData = tweetsFormatted.formatTweets(theTweets.newTweetData)
        makeTweets.makeModelFromList(theTweets.newTweetData)

        tweets = makeTweets.generateTweetsFromModel(20)
        # test if this is the problem
        finalTweets = {'theTweets': tweets}
        self.response.write(json.dumps(finalTweets))


class Testing(webapp2.RequestHandler):
    def get(self, username):
        auth = tweepy.OAuthHandler(twittercreds.consumerKey, twittercreds.consumerSecret)
        auth.set_access_token(twittercreds.accessToken, twittercreds.accessTokenSecret)
        api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
        userData = api.get_user(username)


        self.response.write(json.dumps(userData))



allowed_methods = webapp2.WSGIApplication.allowed_methods
app = webapp2.WSGIApplication([
    ('/test/(.*)', Testing),
    ('/tweets', TweetMaker),
    ('/tweets/(.*)', TweetMaker),
    ('/secret', SecretHandler)
], debug=True)
