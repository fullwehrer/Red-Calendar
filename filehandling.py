import csv
import pandas as pd
from datetime import timedelta, date
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

def createentry(savefile, year, month, day, first, blood, pain, painkiller, forgot):
        
        
        with open(savefile, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([year, month, day,first, blood, pain, painkiller, forgot])
        f.close()

def orderbydate(savefile):
    filedata=pd.read_csv(savefile, header=None)
    filedata.sort_values([filedata.columns[0],filedata.columns[1],filedata.columns[2]], axis=0, ascending=[True,True, True], inplace=True)
    filedata.to_csv(savefile, index=False, header=False)

def checkentryexists(savefile, year, month, day):
    
    with open(savefile, 'r', newline='') as f:
        reader = csv.reader(f)
        rownumber=-1
        result = [False,rownumber]
        for row in reader:
            rownumber=rownumber + 1
            rowyear=int(row[0])
            rowmonth=int(row[1])
            rowday=int(row[2])
            if rowyear==year and rowmonth==month and rowday== day:
                result = [True,rownumber]
        print(result)
        return result    
    f.close()

def deleteentry(savefile, rownumber):
    filedata=pd.read_csv(savefile, header=None)
    # filedata.drop([rownumber])
    filedata = filedata.drop(rownumber)
    filedata.to_csv(savefile, index=False, header=False)

def fillpast(savefile, year, month, day, kind):
    if kind == 'zeros':
        filler = 0
    elif kind == 'forgotten':
        filler = -1
    else:
        print('error fillpast')
        return
    pastdates=daterange(date(2022,7,1),date(year,month,day))
    pastdates.reverse()
    filedata=pd.read_csv(savefile, header=None)
    fillentries=[]
    print(filedata)
    for single_date in pastdates:
        for i in range(len(filedata)):
            rowyear=int(filedata.iloc[i,0])
            rowmonth=int(filedata.iloc[i,1])
            rowday=int(filedata.iloc[i,2])
            if rowyear==single_date[0] and rowmonth==single_date[1] and rowday==single_date[2]:
                break
            else:
                fillentries.append([single_date[0], single_date[1], single_date[2],False, filler, filler, False, False])
    fillentries=pd.DataFrame(fillentries)
    filedata=pd.concat([filedata,fillentries],ignore_index=False)
    print(filedata)
    filedata.to_csv(savefile, index=False, header=False)

def daterange(start_date, end_date):
    pastdates=[]
    for n in range(int ((end_date - start_date).days)):
        currentdate=start_date + timedelta(n)
        pastdates.append([currentdate.year, currentdate.month, currentdate.day])
    return pastdates