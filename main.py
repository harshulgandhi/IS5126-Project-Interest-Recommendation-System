from FirstClass import FirstClass
from TFIDF import TFIDF
import cmath
fc_obj = FirstClass()
txt = "This is NLTK Tutorial"

#print type(cmath.log(3/4))
 
fc_obj.sampleNltk(txt) 
testList = ["hockey","liberty","toi_text"]
refinedList = fc_obj.stopWords(fc_obj.openFile(testList))
freqDictionary = fc_obj.calculateTfidf(refinedList)
print freqDictionary



# f = open("SampleFiles/test.txt","w+")
# print f.read()
# f.seek(0)
# f.write("this was test file")
# f.seek(0)
# print f.read()


