import csv
import pandas as pd
from datetime import timedelta, date
from os.path import exists
import wx
def getpastentries(savefile):
    pastentries = []
    f = open(savefile)
    limit=200
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
    
    
    reader =pd.read_csv(savefile, header=None)
    return checkentryexists_dataframesub(reader, year, month, day)
    

def checkentryexists_dataframesub(dataframe, year, month, day):
        rownumber=-1
        result = [False,rownumber]
        for i in range(len(dataframe)):
            rownumber=rownumber + 1
            rowyear=int(dataframe.iloc[i,0])
            rowmonth=int(dataframe.iloc[i,1])
            rowday=int(dataframe.iloc[i,2])
            if rowyear==year and rowmonth==month and rowday== day:
                result = [True,rownumber]
        #print(result)
        return result    

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
    pastdates=daterange(date(2022,1,1),date(year,month,day))
    pastdates.reverse()
    filedata=pd.read_csv(savefile, header=None)
    fillentries=[]
    alreadyexists = False
    # print(pastdates)
    for single_date in pastdates:
        for i in range(len(filedata)):
            rowyear=int(filedata.iloc[i,0])
            rowmonth=int(filedata.iloc[i,1])
            rowday=int(filedata.iloc[i,2])
            if rowyear==single_date[0] and rowmonth==single_date[1] and rowday==single_date[2]:
                alreadyexists=True
            
        if alreadyexists:
            break
        else:
            fillentries.append(fillerentry(single_date[0], single_date[1], single_date[2], filler))

    fillentries=pd.DataFrame(fillentries)
    filedata=pd.concat([filedata,fillentries],ignore_index=True)
    # print(filedata)
    filedata.to_csv(savefile, index=False, header=False)

def fillerentry(year, month, day, filler):
    return [year, month, day,False, filler, filler, False, False]


def daterange(start_date, end_date):
    pastdates=[]
    for n in range(int ((end_date - start_date).days)):
        currentdate=start_date + timedelta(n)
        pastdates.append([currentdate.year, currentdate.month, currentdate.day])
    return pastdates

def checkcreatesavefile(savefile):
    if not exists(savefile):
        tmpapp = wx.App(redirect=False)
        
        popup=wx.MessageDialog(None, 'No savefile "redcalendar.csv" found in this directory. Create new one? Program will close and needs to be restarted manually.', 'Note', wx.YES_NO).ShowModal()
        tmpapp.MainLoop()
        if popup == wx.ID_YES:
            f=open(savefile, 'w')
            f.close()
            createentry(savefile, 2022, 1, 1, False, 0, 0, False, False)
            exit()
        else:
            exit()
