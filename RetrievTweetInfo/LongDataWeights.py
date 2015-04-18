import csv
import random
import time

MAXUSERS = 1000
class DataGenerator:
    def __init__(self):
        self.placeTypeFile = "place types and image concepts.csv"
        self.placeTypeLongi = "place types and image concepts_Longitudinal.csv"
        
    
    def loadPlaceTypes(self): 
        f_r= open(self.placeTypeFile)
        reader = csv.reader(f_r,delimiter=' ',quotechar='|',quoting =csv.QUOTE_MINIMAL)
        f_r= open(self.placeTypeLongi)
        reader_L = csv.reader(f_r,delimiter=' ',quotechar='|',quoting =csv.QUOTE_MINIMAL)
        
        with open (self.placeTypeFile,'ab') as f_w:
            csvwrite = csv.writer(f_w,delimiter=',',quotechar='|',quoting =csv.QUOTE_MINIMAL)
            self.addSampleRow(csvwrite, reader, 97)
            
        with open (self.placeTypeLongi,'ab') as f_w_L:
            csvwrite_L = csv.writer(f_w_L,delimiter=',',quotechar='|',quoting =csv.QUOTE_MINIMAL)
            self.addSampleRowLongi(csvwrite_L, reader_L, 98)

    '''
    Sample data generator
    '''
    def addSampleRow(self,csvwrite,csvreader,length):
        for i in range(1,MAXUSERS,1):
            eachrow=[]
            for j in range(0,length,1):
                if j == 0:
                    eachrow.append("user"+str(i))
                else:
                    eachrow.append(str(round(random.uniform(0,1),3)))
            print eachrow
            csvwrite.writerow(eachrow)
            eachrow = []
            
    '''
    Sample data generator
    '''
    def addSampleRowLongi(self,csvwrite_L,csvreader_L,length):
        for i in range(1,MAXUSERS,1):
            for k in range(0,24,1):
                eachrow=[]
                
                for j in range(0,length,1):
                    if j == 0:
                        eachrow.append("user"+str(i))
                    elif j == 1:
                        eachrow.append(str(k))
                    else:
                        eachrow.append(str(random.randint(0,500)))
                print eachrow
                csvwrite_L.writerow(eachrow)
                eachrow = []
    
    '''
    Function to return a vector of 96 dimension
    with normalized weight for each place type 
    @param username : username for which vector is needed
    @param timeOfDay : hour of day  
    '''
    def getPlaceTypeWeights(self,username,timeOfDay):
#         username = raw_input("Enter user name : ")
#         timeOfDay = raw_input("Enter time of day for which you need the vector")
        with open (self.placeTypeLongi,'r') as f_r_L:
            csvreader_L = csv.reader(f_r_L,delimiter=',',quotechar='|',quoting =csv.QUOTE_MINIMAL)
#             headers = csvreader_L.next()

            for eachrow in csvreader_L:
                if eachrow[0] == username and self.unixTimeToDayHour(eachrow[1]) == timeOfDay:
                    sum = 0
                    print eachrow
                    #first calculating the sum for that hour for the queried user
                    for i in range (2,98):
                        sum = sum + int(eachrow[i])
                    print sum
                    #calculating the weights and return the vector
                    for i in range (2,98):
                        eachrow[i] = float(eachrow[i])/sum
                        
                    #removing time of day and username from vector
                    eachrow.remove(eachrow[0])
                    eachrow.remove(eachrow[0])
                    return eachrow

    def unixTimeToDayHour(self,unixT):
        return time.strftime("%H",time.localtime(int(unixT)))




def main():
    dgo = DataGenerator()
    ##DO NOT run sample data generator again
    #dgo.loadPlaceTypes()
    print dgo.getPlaceTypeWeights('user1','13')


if __name__=="__main__": main()
    
    