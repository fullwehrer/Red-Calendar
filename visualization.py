
from copy import deepcopy
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
import pandas as pd
import calendar
import filehandling

from filehandling import checkentryexists



def visualize(savefile):
    savefile='visualizationtesting.csv'
    fordate=dt.today()
    preparedata(savefile, fordate)
    
    

def somemonthsago(fordate):
    datevar=fordate
    months = []
    for delta_month in range(6):
        months.append(datevar.month)
        datevar=date(datevar.year, datevar.month, 1)
        delta=timedelta(days=1)
        datevar=datevar-delta
    return datevar, months   

def preparedata(savefile, fordate):
    filedata=pd.read_csv(savefile, header=None)
    cutoff, observedmonths=somemonthsago(fordate)
    filedata=filedata[filedata[0] >= cutoff.year]
    filedata=filedata[~((filedata[0] == cutoff.year) & (filedata[1] <=cutoff.month))]
    daysinmonth=calendar.monthrange(fordate.year, fordate.month)[1]
    for i_day in range(daysinmonth):
        if not (filehandling.checkentryexists_dataframesub(filedata, fordate.year, fordate.month, i_day+1)[0]):
            filedata=pd.concat([filedata,pd.DataFrame(filehandling.fillerentry(fordate.year, fordate.month, i_day+1, -1)).T],ignore_index=True)
            
    
    return filedata,observedmonths

def plot(savefile, fordate):
    plotdata, observedmonths=preparedata(savefile, fordate)
    return


visualize('visualizationtesting.csv')