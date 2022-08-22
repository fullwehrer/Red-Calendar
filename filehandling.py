import csv
import pandas as pd
def getpastentries(savefile):
    pastentries = []
    f = open(savefile)
    limit=100
    counter=0
    rowcount = sum(1 for line in f)
    if rowcount > limit:
        skip = rowcount - limit
    else:
        skip = 0
    with open(savefile, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if counter >= skip:
                    strlist=row[0:3]
                    intlist=[eval(i) for i in strlist]
                    pastentries.append(intlist)
                counter = counter + 1
    f.close()
    return(pastentries)

def createentry(savefile, year, month, day, first, blood, pain, painkiller):
        
        
        with open(savefile, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([year, month, day,first, blood, pain, painkiller])
        f.close()

def orderbydate(savefile):
    filedata=pd.read_csv(savefile, header=None)
    filedata.sort_values([filedata.columns[0],filedata.columns[1],filedata.columns[2]], axis=0, ascending=[True,True, True], inplace=True)
    filedata.to_csv(savefile, index=False, header=False)

def checkentryexists(savefile, year, month, day):
    with open(savefile, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]==year and row[1]==month and row[2]== day:
                return True
            else:
                return False
    f.close()

# def fillzeros(date):