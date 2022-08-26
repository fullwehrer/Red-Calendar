
from cProfile import label
from copy import deepcopy
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
from tkinter.ttk import Style
from turtle import color
import pandas as pd
import calendar
import filehandling
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import ticker
from matplotlib import offsetbox as ob




def visualize(savefile):
    savefile='visualizationtesting.csv'
    # fordate=dt.today()
    fordate=date(2022,9,5)
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
    text1=('Bleeding: 0-no blood, 1-spotting, 2-light bleeding, 3-medium bleeding, 4-stronger bleeding, 5-heavy bleeding')
    text2=("Pain: Mankoski Pain Scale - http://www.valis.com/andi/painscale.html (e.g. 0-pain free, 5-can't be ignored for more than 30 min, 10-pain makes you pass out)")
    
    
    
    fig=plt.figure(figsize=(15,7.5))
    # plt.text(-0.1,-0.1,text1, fontsize=18, style='oblique', ha='center',
    #      va='top', wrap=True)
    
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
        
        positioning_painkiller=pain-1
        positioning_first=pd.DataFrame([0.5]*len(first))
        positioning_nodata=pd.DataFrame([10]*len(nodata))
        

        painkillerdata=pd.concat([x, positioning_painkiller, painkiller], axis=1).reset_index(drop=True)
        painkillerdata.columns=range(painkillerdata.shape[1])
        painkillerdata=painkillerdata[painkillerdata[2]== True]

        firstdata=pd.concat([x, positioning_first, first], axis=1).reset_index(drop=True)
        firstdata.columns=range(firstdata.shape[1])
        firstdata=firstdata[firstdata[2]== True]

        nodatadata=pd.concat([x, positioning_nodata, nodata], axis=1).reset_index(drop=True)
        nodatadata.columns=range(nodatadata.shape[1])
        nodatadata=nodatadata[nodatadata[2]== -1]

        

        ax2=a.twinx()
        
        bleedplot=ax2.bar(x-0.2, blood, 0.4, color='red', label='bleeding amount')
        painplot=a.bar(x+0.2, pain, 0.4,color='black', label='pain amount')
        painkillerplot=a.scatter(painkillerdata[0]+0.2, painkillerdata[1], color='steelblue', marker='X', label='painkiller taken')
        firstplot=ax2.scatter(firstdata[0]-0.1, firstdata[1], color='cyan', marker=5, label='first day of period')
        nodataplot=a.bar(nodatadata[0], nodatadata[1], color='0.9', label='no data')
        plotcollection=[bleedplot, painplot, painkillerplot, firstplot, nodataplot]
        a.grid(axis='both')
        a.set_xlim(0.3,32)
        a.set_ylim(0,10)
        ax2.set_ylim(0,5)
        a.set_ylabel(date(2000,observedmonths[i_month],1).strftime("%b"))
        a.set_xlabel('day of the month')
        if i_month!=len(observedmonths)-1:
            a.xaxis.set_major_formatter(ticker.NullFormatter())
        if i_month==0:
            plt.legend(plotcollection, [p_.get_label() for p_ in plotcollection],bbox_to_anchor=(0,1,1,.1), ncol=5, mode="expand", loc="lower left")
        # if i_month==len(observedmonths)-1:
        #     plt.legend('wfwefg',bbox_to_anchor=(0,0,1,.1), ncol=1, mode="expand", loc="upper left")
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
    plt.show()




    return


visualize('visualizationtesting.csv')