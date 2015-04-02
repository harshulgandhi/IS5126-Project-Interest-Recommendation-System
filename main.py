from FirstClass import TFIDF,TweetTfidf
from TFIDF import TFIDF
import cmath
from os import listdir

fc_obj = TweetTfidf()
txt = "This is NLTK Tutorial"

# data = {1:'a', 2:'b'}
# print "type => ",type(data)
# print "sorted(data.values()) =>",sorted(data.values())
# print "sorted(data, key=data.get) =>",sorted(data, key=data.get)
# print "sorted(data.items(), key=lambda x:x[1]) => ",sorted(data.items(), key=lambda x:x[1], reverse=True)
# 
# print "type(sorted(data.items(), key=lambda x:x[1]) => ",type(sorted(data.items(), key=lambda x:x[1]))



fc_obj.sampleNltk(txt) 
 
fileList = fc_obj.getFileList("Tweets/")
print "fileList == ", fileList
refinedList = fc_obj.stopWords(fc_obj.openFile(fileList))
 
freqDictionary = fc_obj.calculateTfidf(refinedList)
#print freqDictionary



# f = open("SampleFiles/test.txt","w+")
# print f.read()
# f.seek(0)
# f.write("this was test file")
# f.seek(0)
# print f.read()


