from nlp.tokenizer import Tokenizer
from nlp.nlputil import NlpUtilities
from nltk import word_tokenize
import csv
from pip._vendor.distlib.util import CSVWriter
DEBUG = True

class TweetProcessor:
    
    def __int__(self):
        'this class applies tokenization and nlputilities on all the tweets'
        
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
        
    
    def nlp_util(self,text):
        try:
            nlpobj = NlpUtilities()
            text = nlpobj.replace_repeated_letters(text, 2,1)
            text = nlpobj.clean_tweet(text)
            text = word_tokenize(text, 'english')
            text = nlpobj.remove_stopwords(text)
            temp = ''
            for i in range(0,len(text)):
                if i != 0:
                    temp = temp +" "+ text[i]
                else:
                    temp = text[i]
            return temp
        except UnicodeDecodeError:
            print "Unicode decode error found"
    def tokenizer(self, text):
        t_obj = Tokenizer(text)
        t_obj.tokenize_as_tweet()
        return t_obj.get_token_list()
        
    
    def processTweetDict(self,d):
        header=['username','text','tokenized_tweet','processed_tweet','timestamp','geo','media_exists']
        fl= open('processed_tweet.csv',"wb")
        csvwriter = csv.DictWriter(fl,delimiter=",",fieldnames=header)
        csvwriter.writerow(dict((fn,fn) for fn in header))
        print "Creating output file..."
        for row in d:
            tmp = self.nlp_util(row['text'])
            row['processed_tweet']= tmp
            row['tokenized_tweet']= self.tokenizer(tmp)
            csvwriter.writerow(row)
        print "output file has been created!"
        
#     def writeOutputToFile(self,d):
#         header=['username','text','tokenized_tweet','processed_tweet','timestamp','geo','media_exists']
#         fl= open('processed_tweet.csv',"wb")
#         csvwriter = csv.DictWriter(fl,delimiter=",",fieldnames=header)
#         csvwriter.writerow(dict((fn,fn) for fn in header))
#         for row in d:
#             csvwriter.writerow(row)
#         print "output file has been created!"
#         fl.close()
# #             row['processed_tweet'] = row['text']
# #             print row['username'] + " == "+ row['text']+ " == "+row['geo']+ " == "+row['timestamp']+ " == "+row['processed_tweet'] 

if __name__ == "__main__":
    print "Running tweet processor"
    tp_obj = TweetProcessor()
    dataDict = tp_obj.readFile('t_text_loc_time_media.csv')
    print tp_obj.nlp_util('Hiii whats uppp tomorrrrow')
    
    tp_obj.processTweetDict(dataDict)
    
    