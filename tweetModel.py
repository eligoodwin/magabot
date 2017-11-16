import markovify
import json
import codecs

class DotardTweets():
    corpusTxt = ""
    modelFileName = 'trumpModel.json'
    textModel = []

    def makeModelFromList(self, tweetDict):
        """Make a model from tweets still in dict form"""
        corpusTxt = []
        for i in range(len(tweetDict)):
            corpusTxt.append(tweetDict[i]['text'])
        self.textModel = markovify.Text(corpusTxt, state_size=3)

        # with open(self.modelFileName, 'w') as outFile:
        #     json.dump((dict(textModel), outFile))

        # outFile.close()


    def makeTextFileFromJsonFile(self, JSONfilename):
        """converts the json to a txt file that is used as the corpus"""
        #get json data and convert it to text
        with open(JSONfilename) as fileIn:
            jsonData = json.load(fileIn)
        length = len(jsonData)
        fileIn.close()

        with codecs.open(self.corpusTxt, "a", "utf-8-sig") as writeFile:
            for i in range(length):
                writeFile.write(jsonData[i]['text'])
        writeFile.close()


    def makeTextFromData(self, data):
        """Pass tweet data directly in and construct the txt file used to construct the model"""
        length = len(data)
        with codecs.open(self.corpusTxt, "a", "utf-8-sig") as writeFile:
            for i in range(length):
                writeFile.write(data[i]['text'])
        writeFile.close()


    def setCorpusFileName(self, fileName):
        self.corpusTxt = fileName


    def createModelFromTxtFile(self):
        """takes a txt file of tweets and contructs the model and writes it to file"""
        with open(self.fileName) as fileIn:
            text = fileIn.read()
        self.textModel = markovify.Text(text, state_size=2)
        modelJson = self.textModel.to_json()
        with open(self.modelFileName, 'w') as outFile:
            json.dump(modelJson, outFile)



    def generateTweetsFromModel(self, number):
        pseudoTweets = []
        for i in range(number):
            newTweet = self.textModel.make_short_sentence(70)
            while(newTweet is None):
                newTweet = self.textModel.make_short_sentence(70)
            newTweet2 = self.textModel.make_short_sentence(70)
            while (newTweet2 is None):
                newTweet2 = self.textModel.make_short_sentence(70)
            pseudoTweets.append(newTweet + " " + newTweet2)
        return pseudoTweets


    def importModel(self, fileName):
        """imports the model from the json and returns it"""
        with open(fileName) as dataFile:
            tweetModel = json.load(dataFile)
        return markovify.Text.from_json(tweetModel)


    def generateTweetCollection(self):
        #import model
        tweetModel = self.importModel(self.modelFileName)
        tweets = self.generateTweetsFromModel(tweetModel, 20)

        return tweets

