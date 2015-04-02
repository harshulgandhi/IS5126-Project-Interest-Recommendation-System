from TFIDF import TFIDF
import nltk
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from idlelib import PathBrowser
from os import listdir
from os.path import isfile, join

class TweetTfidf:
	stop = []
	debug = False
	listDict = []
	inputList = []
	
	def __init__(self):
		print 'Inside first class'
		self.stop = stopwords.words('english')
		
	def getFileList(self,path):
# 		[f for f in listdir(path)]
# 		print "len(f) = ",len(f)
 		self.inputList = listdir(path)
		return self.inputList
	
	
	def sampleNltk(self,str):
		words = word_tokenize(str)
		print "Tokenizer example"
		print words
		refined = [i for i in words if i not in self.stop] 
		print "Words after removing stop words"
		if self.debug:
			print refined
		
	def openFile(self,fileList):
		listFile =[]
		for i in range(0,len(fileList),1):
			name = "Tweets/"+fileList[i]
			file = open(name,"r+")
			file.seek(0)
			listFile.append(file)
		return listFile
			
	def stopWords(self,fileList):
		listFile = []
		for i in range(0,len(fileList),1):
			words = word_tokenize(fileList[i].read().decode('UTF-8'), 'english')
			if self.debug:
				print words
			words = [x for x in words if x not in self.stop]
			if self.debug:
				print "WITHOUT STOP WORDS ==> ",words
			listFile.append(words)
		return listFile
	
	def calculateTfidf(self,docList):
		idfObj = TFIDF()
# 		[l for l in listdir("Tweets/") if isfile(join("Tweets/",l))]
# 		print "f[0] => ",l
		for i in range(0,len(docList),1):
			freqDict = {}
			file = open("Tweets/tfidf_"+self.inputList[i],"w+")
			print "File open with name : "+"tfidf"+self.inputList[i]
			for j in range(0,len(docList[i]),1):
				freqDict[docList[i][j]] = idfObj.tfidf(docList, docList[i], docList[i][j]) 
				
			self.listDict.append(freqDict)
			sortedFreqList = sorted(freqDict.items(),key=lambda x:x[1],reverse=True)
			for k in range(0,len(sortedFreqList),1):
				file.write(str(sortedFreqList[k]))
				file.write("\n")
			print "TFIDF for tweeter account "+str(self.inputList[i])+" has been created\n" 
				
		return self.listDict