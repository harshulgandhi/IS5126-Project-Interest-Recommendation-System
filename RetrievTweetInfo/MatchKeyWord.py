import csv
import random
import time

MAXUSERS = 1000
class MatchKeyWord:
    def __init__(self):
        
        self.placeTypeFile = "PlaceTypeswKeyWords.csv"
        self.placeTypeMatch ={}
    
    '''
    Function to return number of match for a placetype
    based on given key words
    '''
        
    def readPlaceTypes(self,inputList):
        f_r= open(self.placeTypeFile)
        reader_L = csv.reader(f_r,delimiter=',',quotechar='|',quoting =csv.QUOTE_MINIMAL)
        placeTypeList = []
        for eachrow in reader_L:
            currPlaceType = eachrow[0]
#             print "currPlaceType ==> ",type(currPlaceType)
            placeTypeList.append(currPlaceType)
            eachrow.remove(currPlaceType)           #this is to get the list of keywords corresponding to a placetype so that searching becomes easier
            count = 0
            for eachword in inputList:
                
                if eachword in eachrow:
                    count = count + 1
            if count > 0:
                self.placeTypeMatch[currPlaceType] = count
            count = 0         
        
        return self.placeTypeMatch
        
        
        
        
def main():
    inputList = ['dipping','colada','hoodies','snickers','suit']
    matchO = MatchKeyWord()
    print matchO.readPlaceTypes(inputList)


if __name__=="__main__": main()