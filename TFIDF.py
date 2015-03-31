import math 
class TFIDF:
    
    def __init__(self):
        print 'To calculate tfidf score'
    
    '''
    computes "term frequency" 
    which is the number of times a word appears 
    in a document doc, normalized by dividing 
    by the total number of words in doc. 
    '''
    def termFrequency(self,doc,word):
        return float(doc.count(word))/len(doc)
    
    '''
    returns the number of documents containing word
    '''
    def countContaining(self,docList,word):
        return sum (1 for doc in docList if word in doc)
    
    '''
     computes "inverse document frequency" which 
     measures how common a word is among 
     all documents in doclist.
    ''' 
    def idf(self,docList,word):
        c_doc = self.countContaining(docList, word)
        if c_doc <= 0:
            return math.log(len(docList)/(1 + c_doc))
        else:
            return math.log(len(docList)/c_doc)    
        
    
    '''
     computes the TF-IDF score. 
     It is simply the product of tf and idf.
    '''
    def tfidf(self,docList,doc,word):
        return self.termFrequency(doc, word)*self.idf(docList,word)
    
    