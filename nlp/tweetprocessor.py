from nlp.tokenizer import Tokenizer
from nlp.nlputil import NlpUtilities
from nltk import pos_tag
from nltk import word_tokenize
from geolocation import GeoLocation
import csv
from pip._vendor.distlib.util import CSVWriter
import numpy
import re, collections
import spellcorrect
#from setuptools.tests import textwrap
from tarfile import ReadError

DEBUG = True

class TweetProcessor:
    wordList = set()
    slangDict = {}    
    def __init__(self):
        'this class applies tokenization and nlputilities on all the tweets'
        self.createSlangDict()
        self.NWORDS = self.train(self.words(file('big.txt').read()))
        self.wordList =  set(open('UKACD17.TXT').read().split())
        
    
    def loadSpelCheckFile(self):
        return self.train(self.words(file('big.txt').read()))
    
    '''
    These two methods are for spellcorrect functionality
    '''
    def words(self,text): return re.findall('[a-z]+', text.lower()) 

    def train(self,features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

        
    #reads csv and returns a dictionary of the data
    def readFile(self,fileName):
        d = {}
        d['username'] = []
        d['text'] = []
        d['geo'] = []
        d['timestamp'] = []
        d['media_exists'] = []
        f = open(fileName,"rb")
        csv_fdict = csv.DictReader(f)
#         csv_fdict = csv.DictReader(f,fieldnames=['username','text','geo','timestamp','media_exists'],delimiter=',',quotechar='"')
#         for row in csv_fdict:
#             for key in row:
#                 d[key].append(row[key])
#         if DEBUG:
#             print len(d)
        return csv_fdict
        
    
    def createSlangDict(self):
        print "creatng dict"
        f= open("inet-slangs-words.txt")
        reader = csv.reader(f,delimiter="\t")
        lst = list(reader)
        for i in range (0,len(lst),1):
            self.slangDict[lst[i][0]] = lst[i][1]
            
            
    def replaceInetSlang(self,text):
        textLst = text.split()
        for i in range(0,len(textLst)):
            if textLst[i] in self.slangDict.keys():
                textLst[i] = self.slangDict[textLst[i]]
                
        return self.listToString(textLst)
            
        
        
    def listToString(self,text):
        temp = ''
        for i in range(0,len(text)):
            if i != 0:
                temp = temp +" "+ text[i]
            else:
                temp = text[i]
        return temp
    
    
    def spellCorrector(self,text):
        textLst = text.split()
        temp = []
        for i in range(0,len(textLst)):
            if self.checkInWordList(textLst[i]):
                temp.append(textLst[i])
            else:
                temp.append(spellcorrect.correct(textLst[i], self.NWORDS))
        return self.listToString(temp)
        
    
    def checkInWordList(self,word):
        return word.lower() in self.wordList
    
    def nlp_util(self,text):
        try:
            nlpobj = NlpUtilities()
            text = nlpobj.replace_repeated_letters(text, 2,1)
            #add code to replace internet slangs
            text = self.replaceInetSlang(text)
            #to correct spelling
            text = self.spellCorrector(text)
                        
            text = nlpobj.clean_tweet(text)
            text = word_tokenize(text, 'english')
            text = nlpobj.remove_stopwords(text)
            return self.listToString(text)
        except UnicodeDecodeError:
            print "Unicode decode error found"
            
            
    def tokenizer(self, text):
        t_obj = Tokenizer(text)
        t_obj.tokenize_as_tweet()
        tokenList = t_obj.get_token_list()
        l = len(tokenList)
        i = 0
        tokenizedWord = []
        while i < l:
            if tokenList[i][1] != 10 or tokenList[i][0] == '@':
                tokenList.remove(tokenList[i])
                l=l-1
            else:
                tokenizedWord.append(tokenList[i][0])
                i+=1
            
        return tokenizedWord
        
    def stringToList(self,lst):
        tmp = ''
        geo = ()
        for i in range(0,len(lst),1):
            if(lst[i] == ' '):
                j = i+1
                while j< len(lst) and  lst[j] != ',' and lst[j] != ' ':
                    if lst[j] == ']':
                        return geo
                    tmp += lst[j]
                    j+=1
                geo = geo +(float(tmp),)   
                i = j
                tmp =''
                
        print geo
        #print "type(geo) ",type(geo)
        return geo
        
    def processTweetDict(self,d):
        header=['username','text','tokenized_tweet','processed_tweet','nouns_per_tweet','timestamp','geo','media_exists']
        fl= open('processed_tweet.csv',"wb")
        csvwriter = csv.DictWriter(fl,delimiter=",",fieldnames=header)
        userLocation = {}
        
        csvwriter.writerow(dict((fn,fn) for fn in header))
        print "Creating output file..."
        count = 0
        for row in d:
            count += 1
            tmp = self.nlp_util(row['text'])
            x = list(row['geo'])
            row['processed_tweet']= tmp
            
            tokenizedList = self.tokenizer(tmp)
            row['tokenized_tweet']= tokenizedList 
            
            postaggedList = pos_tag(tokenizedList)
            
            #to tag words and extract nouns
            nounList = [word for word,pos in postaggedList if pos.find('NN')>-1]
            row['nouns_per_tweet']= nounList 
            
            if str(row['username']) in userLocation.keys():
                #print "found key"
                userLocation[row['username']].append(self.stringToList(row['geo']))
            else:
                userLocation[str(row['username'])] = [self.stringToList(row['geo'])]
            csvwriter.writerow(row)
            print "Processed tweet no : ",count
            
        print "output file has been created!"
        #print userLocation
        return userLocation         
    
    def tweetPerLocation(self, userDict):
        countPerLocation = {}
        
        for user in userDict.keys():
            ln = len(userDict[user])
            i = 0
            while i < ln-1:
            
                count = 0
                avg = userDict[user][i]
                p1 = GeoLocation.from_degrees(avg[0], avg[1])
                
                j = i
                while j < ln:
                    p2 = GeoLocation.from_degrees(userDict[user][j][0], userDict[user][j][1])
                    if p1.distance_to(p2) < 0.02:
                        avg = [(avg[0]+userDict[user][j][0])/2,(avg[1]+userDict[user][j][1])/2]
                        count += 1
                        userDict[user].remove(userDict[user][j])
                        ln = ln-1
                    j += 1
                if user in countPerLocation.keys():
                    countPerLocation[user].append((avg,count))
                else:
                    countPerLocation[user] = [(avg,count)]
                i+=1
                
        ##Code to write results to a csv file
        f = open("tweetPerLocation.csv","wb")
        csvf = csv.writer(f,delimiter=",")
        for user in countPerLocation.keys():
            ln = len(countPerLocation[user])
            eachrow=[]
            for i in range(0,ln):
                eachrow.append(user)
                eachrow.append(countPerLocation[user][i][0])
                eachrow.append(countPerLocation[user][i][1])
                csvf.writerow(eachrow)
                eachrow=[]


if __name__ == "__main__":
    print "Running tweet processor"
    tp_obj = TweetProcessor()
    dataDict = tp_obj.readFile('t_text_loc_time_media.csv')
    NWORDS = tp_obj.train(tp_obj.words(file('big.txt').read()))
    userLocation = tp_obj.processTweetDict(dataDict)
    countPerLocation = tp_obj.tweetPerLocation(userLocation)
     
