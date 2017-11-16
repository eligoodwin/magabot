import tweepy
import json
import io
import twittercreds

#get the tweets of the
class Tweets():
    newTweetData = [] #an array holding the


    def __init__(self, userName, lastTweetId):
        self.userName = userName
        self.lastTweetId = lastTweetId


    def __init__(self, userName):
        self.screenName = userName


    def getLotsOfTweets(self):
        #authorize twitter
        auth = tweepy.OAuthHandler(twittercreds.consumerKey, twittercreds.consumerSecret)
        auth.set_access_token(twittercreds.accessToken, twittercreds.accessTokenSecret)
        api = tweepy.API(auth)

        #this is howe the tweeting bullshit works. It gets the--it comes in as a josn formatted str
        #the problem is that we can deal with it yet

        self.newTweetData = self.makeToList(api.user_timeline(screen_name=self.screenName, count=200))

        #get length of newTweets
        #if lenght == 200, get more tweets until length is no longer 200 or total length is 3000
        length = len(self.newTweetData)
        newTweets = []

        if length == 200:
            #make request for last tweet
            while length == 200 and len(self.newTweetData) < 3600:
                lastTweetId = self.newTweetData[-1]['id_str']
                tempTweets = api.user_timeline(screen_name=self.screenName, count=200, max_id=lastTweetId)
                #convert to json then to dict
                newTweets = self.makeToList(tempTweets)
                self.newTweetData += newTweets
                length = len(newTweets)
        # jsonTweets = json.dumps([status._json for status in newTweets])
        # #now we can load it up and treat as json
        # self.newTweetData = json.loads(jsonTweets)
        print len(self.newTweetData)


    def getRecentTweets(self):
        auth = tweepy.OAuthHandler(twittercreds.consumerKey, twittercreds.consumerSecret)
        auth.set_access_token(twittercreds.accessToken, twittercreds.accessTokenSecret)
        api = tweepy.API(auth)
        newTweets = api.user_timeline(screen_name=self.screenName, since_id=self.lastTweetId)
        jsonTweets = json.dumps([status._json for status in newTweets])
        self.newTweetData = json.loads(jsonTweets)
        self.lastTweetId = self.newTweetData[0]['id_str']

    def writeTweets(self, outfileName):
        with io.open(outfileName, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.newTweetData, ensure_ascii=False))

    def makeToList(self, inputResult):
        """takes the resulting tweet data coverts it to json, then to a list of dicts"""
        tweetJson = json.dumps([status._json for status in inputResult])
        return json.loads(tweetJson)

    def printTWeets(self):
        for i in range(len(self.newTweetData)):
            print self.newTweetData[i]['text']