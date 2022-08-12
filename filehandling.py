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
    data=pd.read_csv(savefile, header=None)
    data.sort_values([data.columns[0],data.columns[1],data.columns[2]], axis=0, ascending=[True,True, True], inplace=True)
    data.to_csv(savefile, index=False, header=False)