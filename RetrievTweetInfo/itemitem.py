'''
Created on Apr 2, 2015

@author: 9020dell
'''
import csv
import ast
import config
from pymongo import MongoClient


sample_output={}
class ItemItem():
    '''
    classdocs
    '''
    typesDict = {}
    outputList = []
    def __init__(self, amrules):
        '''
        Constructor
        '''
        with open(amrules,'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    valList = self.typesDict[row[2]]
                    valList.append(row[1])
                except:
                    self.typesDict[row[2]] = [row[1]]
    
    def printTypesDict(self):
        print "Total Types: ",len(self.typesDict.keys())
       # self.typesDict = ast.literal_eval(self.typesDict)
        for key in self.typesDict.keys():
#             print key, " :: ", self.typesDict[key]
            combinedList = []
            for sub_L in self.typesDict[key]:
                try:
                    sub_L = ast.literal_eval(sub_L)
                except:
                    pass
#                 print "sub_L ",sub_L
                for each_type in sub_L:
#                     print "each_type ",each_type
                    combinedList.append(each_type) 
            self.typesDict[key] = combinedList
            print combinedList
            combinedList = []
            print key, " :: ", self.typesDict[key]
            
            
    def getMissingPairType(self,amruleList):
        missingTypeList = []
        for each_type in amruleList:
            if each_type not in self.document['agiv']  and each_type not in self.outputList:
                sample_output['agiv'][each_type] = 999
                self.outputList.append(each_type)
        
        
        
    def itemItem(self,document):
        self.document = document
        sample_output['agiv']={}
        for placeType in document['agiv']:
            sample_output['agiv'][placeType] = document['agiv'][placeType] 
            if placeType in self.typesDict:
                self.getMissingPairType(self.typesDict[placeType])
            else:
                for each_type in self.typesDict:
                    if placeType in self.typesDict[each_type]:
                        self.getMissingPairType(self.typesDict[each_type])
 
        for each in sample_output['agiv']:
            print each + " :: "+str(sample_output['agiv'][each]) 
        return self.outputList
if __name__ == "__main__":
#     
    ptl = ItemItem('amrules.csv')
#     ptl.printTypesDict()
#     ptl.itemItem(ptl.typesDict)
#     ptl = ItemItem('C:\\Users\\9020dell\\Documents\\IS5126\\Project\\data\\amrules.csv')
    mongo_client = MongoClient('172.29.24.94', 27017)
    mongo_db_tweetmaster = mongo_client['onespace']
    mongo_coll_tweetmaster_users_find = mongo_db_tweetmaster['twitrec']
    mongo_coll_tweetmaster_users_update = mongo_db_tweetmaster['users']
    for doc in mongo_coll_tweetmaster_users_find.find():
        print doc['_id']
        if doc['_id'] == None:
            continue
        agiv = doc['agiv']
        ptl.printTypesDict()
        print doc
        tt = ptl.itemItem(doc)
        mongo_coll_tweetmaster_users_update.update({'_id': doc['_id']}, { '$addToSet' : {'ii':{'$each':tt} }})
        