import json
import re


class TweetsParser():
    def cleanTweetsFromFile(self, fileName):
        """Passes a filename to a json and returns an array of dicts that can be saved or processed further"""
        with open(fileName) as tweetData:
            unParsedTweets = json.load(tweetData)

        return self.formatTweets(unParsedTweets)


    def cleanTweets(self, tweetText):
        """Cleans tweets of emojis and self referencing of the username.
            Returns the original text clean of character defects"""
        emojiRE = re.compile(u'('
                             u'\ud83c[\udf00-\udfff]|'
                             u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                             u'[\u2600-\u26FF\u2700-\u27BF])+',
                             re.UNICODE)

        noUrlTweet = re.sub(r"http\S+", "", tweetText)
        noSelfMention = re.sub(r"@realDonaldTrump", "", noUrlTweet)
        fixedAmp = re.sub(r'&amp;', "&", noSelfMention)
        removedEmoji = re.sub(emojiRE, " ", fixedAmp)

        text = removedEmoji.decode('utf-8')
        newText = text.encode('ascii', 'ignore')

        return newText

    def deleteKeys(self, tweet):
        """Deletes all the keys in the data that are not needed"""
        keysToKeep = {'text', 'created_at', 'id_str'}
        allKeys = set(tweet.keys())
        keysToDelete = allKeys - keysToKeep
        for unWantedKey in keysToDelete:
            del tweet[unWantedKey]

    def formatTweets(self, tweetData):
        """Joins tweets that are broken up by "...." and rejoins them into one sentence"""
        fixedTweets = []
        preTarget = r'^\.\.\.?\.?\.?'
        postTarget = r'\.\.\.\.?\.?\.?'
        length = len(tweetData)
        for i in range(length):
            self.deleteKeys(tweetData[i])
            if ".." in tweetData[i]["text"]:  # found " " at front
                tweetData[i]['text'] = self.cleanTweets(tweetData[i]['text'])
                stopPoint = i
                tailOfTweet = re.sub(preTarget, " ", tweetData[i]["text"])
                tweetData[i]["text"] = ""
                # build the string up correctly
                if i < length - 1:
                    while ".." in tweetData[i + 1]["text"] and i < length - 1:
                        i += 1
                        tweetData[i]['text'] = self.cleanTweets(tweetData[i]['text'])
                        tempTail = re.sub(preTarget, " ", tweetData[i]["text"])
                        tempTail = re.sub(postTarget, " ", tweetData[i]["text"])
                        tweetData[i]["text"] = ""

                        tailOfTweet = tempTail + tailOfTweet

                tweetData[stopPoint]["text"] = tailOfTweet
                fixedTweets.append(tweetData[stopPoint])

            elif tweetData[i]["text"] != "":
                tweetData[i]['text'] = self.cleanTweets(tweetData[i]['text'])
                fixedTweets.append(tweetData[i])

        return tweetData
