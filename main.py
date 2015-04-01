from FirstClass import FirstClass
from TFIDF import TFIDF
import cmath
fc_obj = FirstClass()
txt = "This is NLTK Tutorial"

 
fc_obj.sampleNltk(txt) 
#testList = ["hockey","liberty","toi_text"]
fileList = fc_obj.getFileList("Tweets/")
print fileList
refinedList = fc_obj.stopWords(fc_obj.openFile(['ConnieSayCheese_tweetdoc.txt']))

freqDictionary = fc_obj.calculateTfidf(refinedList)
print freqDictionary



# f = open("SampleFiles/test.txt","w+")
# print f.read()
# f.seek(0)
# f.write("this was test file")
# f.seek(0)
# print f.read()


