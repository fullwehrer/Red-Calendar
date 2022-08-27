
from copy import deepcopy
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
import pandas as pd
import calendar
import filehandling
from matplotlib import pyplot as plt
from matplotlib import ticker





def visualize(savefile):
    # savefile='visualizationtesting.csv'
    fordate=dt.today()
    # fordate=date(2022,9,5)
    plot(savefile, fordate)
    
    

def somemonthsago(fordate):
    datevar=fordate
    months = []
    for delta_month in range(6):
        months.append(datevar.month)
        datevar=date(datevar.year, datevar.month, 1)
        delta=timedelta(days=1)
        datevar=datevar-delta
    months.reverse()

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
    plotdata=addcounter(plotdata)
    text1=('Bleeding: 0-no blood, 1-spotting, 2-light bleeding, 3-medium bleeding, 4-strong bleeding, 5-heavy bleeding')
    text2=("Pain: Mankoski Pain Scale - http://www.valis.com/andi/painscale.html (e.g. 0-pain free, 5-can't be ignored for more than 30 min, 10-pain makes you pass out)")
    
    
    
    fig=plt.figure(figsize=(15,7.5))

    for i_month in range(len(observedmonths)):
        a=plt.subplot(len(observedmonths), 1,i_month+1)
        x=plotdata[plotdata[1] == observedmonths[i_month]][2].reset_index(drop=True)
        
        first=plotdata[plotdata[1] == observedmonths[i_month]][3].reset_index(drop=True)
        blood=plotdata[plotdata[1] == observedmonths[i_month]][4].reset_index(drop=True)
        nodata=deepcopy(blood)
        blood=blood.replace(-1,0)
        pain=plotdata[plotdata[1] == observedmonths[i_month]][5].reset_index(drop=True)
        pain=pain.replace(-1,0)
        painkiller=plotdata[plotdata[1] == observedmonths[i_month]][6].reset_index(drop=True)
        period=plotdata[plotdata[1] == observedmonths[i_month]][8].reset_index(drop=True)
        cycle=plotdata[plotdata[1] == observedmonths[i_month]][9].reset_index(drop=True)
        lastcycleday=pd.DataFrame(plotdata[plotdata[1] == observedmonths[i_month]][10].reset_index(drop=True))
        
        positioning_painkiller=pain-1
        positioning_first=pd.DataFrame([0.5]*len(first))
        positioning_nodata=pd.DataFrame([10]*len(nodata))
        positioning_period=pd.DataFrame([4]*len(period))
        positioning_cycle=pd.DataFrame([1]*len(cycle))



        

        painkillerdata=pd.concat([x, positioning_painkiller, painkiller], axis=1).reset_index(drop=True)
        painkillerdata.columns=range(painkillerdata.shape[1])
        painkillerdata=painkillerdata[painkillerdata[2]== True]

        firstdata=pd.concat([x, positioning_first, first], axis=1).reset_index(drop=True)
        firstdata.columns=range(firstdata.shape[1])
        firstdata=firstdata[firstdata[2]== True]

        nodatadata=pd.concat([x, positioning_nodata, nodata], axis=1).reset_index(drop=True)
        nodatadata.columns=range(nodatadata.shape[1])
        nodatadata=nodatadata[nodatadata[2]== -1]

        perioddata=pd.concat([x, positioning_period, period], axis=1).reset_index(drop=True)
        perioddata.columns=range(perioddata.shape[1])
        
        cycledata=pd.concat([x, positioning_cycle, cycle], axis=1).reset_index(drop=True)
        cycledata.columns=range(cycledata.shape[1])
        
        

        ax2=a.twinx()
        
        bleedplot=ax2.bar(x-0.2, blood, 0.4, color='red', label='bleeding amount')
        painplot=a.bar(x+0.2, pain, 0.4,color='black', label='pain amount')
        painkillerplot=a.scatter(painkillerdata[0]+0.2, painkillerdata[1], color='steelblue', marker='X', label='painkiller taken')
        # firstplot=ax2.scatter(firstdata[0]-0.1, firstdata[1], color='cyan', marker=5, label='first day of period')
        nodataplot=a.bar(nodatadata[0], nodatadata[1], color='0.9', label='no data')

        for i in range(len(perioddata)):
            periodplot=ax2.text(perioddata.iloc[i,0]-0.3, perioddata.iloc[i,1], perioddata.iloc[i,2])
            if lastcycleday.iloc[i,0]==True:
                cycleplot=ax2.text(cycledata.iloc[i,0]-0.3, cycledata.iloc[i,1], cycledata.iloc[i,2],backgroundcolor='cyan')
            else:
                cycleplot=ax2.text(cycledata.iloc[i,0]-0.3, cycledata.iloc[i,1], cycledata.iloc[i,2])
        

        # plotcollection=[bleedplot, painplot, painkillerplot, firstplot, nodataplot]
        plotcollection=[bleedplot, painplot, painkillerplot, nodataplot]
        a.grid(axis='both')
        a.set_xlim(0.3,32)
        a.set_ylim(0,10)
        ax2.set_ylim(0,5)
        a.set_ylabel(date(2000,observedmonths[i_month],1).strftime("%b"))
        a.set_xlabel('day of the month')
        if i_month!=len(observedmonths)-1:
            a.xaxis.set_major_formatter(ticker.NullFormatter())
        if i_month==0:
            # plt.legend(plotcollection, [p_.get_label() for p_ in plotcollection],bbox_to_anchor=(0,1,1,.1), ncol=5, mode="expand", loc="lower left")
            plt.legend(plotcollection, [p_.get_label() for p_ in plotcollection],bbox_to_anchor=(0,1,1,.1), ncol=4, mode="expand", loc="lower left")
        a.xaxis.set_major_locator(ticker.MultipleLocator(1))
        a.yaxis.set_major_locator(ticker.MultipleLocator(2))
        a.yaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.subplots_adjust(hspace=0.2)
    plt.suptitle('Period Chart')
    plt.text(0,-3,text1, fontsize=10, style='oblique', ha='left',
         va='top', wrap=True)
    plt.text(0,-4,text2, fontsize=10, style='oblique', ha='left',
         va='top', wrap=True)
    plt.savefig('latest_period_chart')
    plt.show()
    

    return

def addcounter(dataframe):
    activeperiod=[]
    cycle=[]
    lastdayofcycle=[]
    counter=0
    for i in range(len(dataframe)):
        lastdayofcycle.append(False)
        if (dataframe.iloc[i,4]==-1): #no data
            periodstate='nodata'
            counter=0
            activeperiod.append('')
            cycle.append('')
        elif (dataframe.iloc[i,4]==0) and (dataframe.iloc[i,5]==0): #time between periods
            if periodstate != 'noperiod':
                periodstate='noperiod'
            counter=counter+1
            activeperiod.append('')
            cycle.append(str(counter))
        else:
            if periodstate != 'period':
                counter=0
                periodstate='period'
                if i>0:
                    lastdayofcycle[i-1]=True
            counter=counter+1
            activeperiod.append(str(counter))
            cycle.append(str(counter))
    dataframe[8]=activeperiod
    dataframe[9]=cycle
    dataframe[10]=lastdayofcycle
    return dataframe
visualize('visualizationtesting.csv')