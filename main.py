from FirstClass import FirstClass
  
fc_obj = FirstClass()
txt = "This is NLTK Tutorial"

fc_obj.sampleNltk(txt) 
testList = ["hockey","liberty","toi_text"]
fc_obj.stopWords(fc_obj.openFile(testList))


f = open("SampleFiles/test.txt","w+")
print f.read()
f.seek(0)
f.write("this was test file")
f.seek(0)
print f.read()


