
import nltk
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class FirstClass:
	stop = []
	debug = True
	
	def __init__(self):
		print 'Inside first class'
		self.stop = stopwords.words('english')
		
	def sampleNltk(self,str):
		words = word_tokenize(str)
		print "Tokenizer example"
		print words
		refined = [i for i in words if i not in self.stop] 
		print "Words after removing stop words"
		print refined
		
	def openFile(self,fileList):
		listFile =[]
		for i in range(0,len(fileList),1):
			name = "SampleFiles/"+fileList[i] + ".txt"
			file = open(name,"r+")
			file.seek(0)
			listFile.append(file)
		return listFile
	
	def stopWords(self,fileList):
		listFile = []
		for i in range(0,len(fileList),1):
			words = word_tokenize(fileList[i].read(), 'english')
			print words
			words = [x for x in words if x not in self.stop]
			if self.debug:
				print "WITHOUT STOP WORDS ==> ",words
			listFile.append(fileList[i])
		return listFile
