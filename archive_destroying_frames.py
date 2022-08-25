#GUI Tutorial used: https://www.blog.pythonlibrary.org/2021/09/29/create-gui/



from time import sleep
import wx
import wx.adv
from datetime import datetime, date
import sys

# print(wx.version())

import filehandling
import visualization



global savefile 
savefile ='visualizationtesting.csv'
quitMyAppLoop=False
now=datetime.today()
globalcalendardate=date(now.year, now.month, now.day)





def getmonthentries(month):
    pastentries=filehandling.getpastentries(savefile)
    pastentries = [row for row in pastentries if row[1]==month]
    result= [row[2] for row in pastentries]
    return(result)


# class Mycalendardateattr(wx.adv.CalendarDateAttr):

#     def __init__ (self):
#         super().__init__(colBack='green')
#         print(self.GetBackgroundColour())




class MyPanel(wx.Panel):
    dateselector=None
    markstyle=None
    
    # markstyle = Mycalendardateattr()

    def unmarkdays(self, dateselector):
        date=self.dateselector.GetDate()
        a=wx.DateTime.GetLastMonthDay(date)
        noofdays=wx.DateTime.GetDay(a)

        for i in range(noofdays):
                if not dateselector.GetAttr(i+1) == None: 
                    dateselector.ResetAttr(i+1)
        self.Show()
        return
        
    def markdays(self, dateselector):
            self.unmarkdays(self.dateselector)
            monthentrylist=getmonthentries(self.month)  
            # print('before deleting')
            # for i in range(31):
            #     # print(dateselector.GetAttr(i+1))
            #     if not dateselector.GetAttr(i+1) == None: 
            #         dateselector.ResetAttr(i+1) 
            # print('after deleting')
            # for i in range(31):
                # print(dateselector.GetAttr(i+1))
            # print('before marking')
            
            for daytomark in monthentrylist:
                # print(dateselector.GetAttr(daytomark))
                # if dateselector.GetAttr(daytomark) == None:
                if True:
                    markstyle=wx.adv.CalendarDateAttr(colBack='green')
                    dateselector.SetAttr(daytomark,markstyle)
            self.Show()
                

    
    
    def __init__(self, parent, calendardate):
        super().__init__(parent)
        

        

        self.year = calendardate.year
        self.month = calendardate.month
        self.day = calendardate.day
        

        # now = datetime.now()
        # self.year = int(now.strftime("%Y")) #default
        # self.month = int(now.strftime("%m")) #default
        # self.day = int(now.strftime("%d")) #default
        self.firstday=False
        self.blood = 0
        self.pain = 0
        self.painkiller = False
        self.forgotcheck=False



        # prev_button = wx.Button(self, label='previous month')
        # prev_button.Bind(wx.EVT_BUTTON, self.on_prev)

        # next_button = wx.Button(self, label='next month')
        # next_button.Bind(wx.EVT_BUTTON, self.on_next)
        
        self.dateselector=wx.adv.GenericCalendarCtrl(self, name="datectrl", date=calendardate)
        self.dateselector.EnableHolidayDisplay(False)
        self.dateselector.EnableMonthChange(True)
        self.dateselector.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,self.on_selectionchanged)
        self.markdays(self.dateselector)
        self.dateselector.Bind(wx.adv.EVT_CALENDAR_PAGE_CHANGED,self.on_pagechanged)

        forgotcheck=wx.CheckBox(self, label="FORGOTTEN? - first entry since longer, forgot to enter last bleeding/pain? (all days from last entry will be marked forgotten)",
            name='forgot_check_box')
        forgotcheck.Bind(wx.EVT_CHECKBOX, self.on_forgotcheck)

        firstcheck=wx.CheckBox(self, label="FIRST entry since last bleeding/pain? (all days from last entry will be marked pain/bloodfree unless FORGOTTEN is also checked)",
            name='firstday_check_box')
        firstcheck.Bind(wx.EVT_CHECKBOX, self.on_firstdaycheck)

        bloodbox=wx.RadioBox(self, label="bleeding amount (0-no blood, 1-spotting, 2 - light bleeding, 3- medium bleeding, 4- stronger bleeding, 5- heavy bleeding)",
            choices=['0','1','2','3','4','5'], majorDimension=0, style=wx.RA_SPECIFY_COLS,
            name='blood_radio_box')
        bloodbox.Bind(wx.EVT_RADIOBOX, self.on_bloodbox)
        painbox=wx.RadioBox(self, label="pain amount (Mankoski Pain Scale - http://www.valis.com/andi/painscale.html)",
            choices=['0','1','2','3','4','5','6','7','8','9','10'], majorDimension=0, style=wx.RA_SPECIFY_COLS,
            name='pain_radio_box')
        painbox.Bind(wx.EVT_RADIOBOX, self.on_painbox)

        painkillercheck=wx.CheckBox(self, label="took painkiller?",
            name='painkiller_check_box')
        painkillercheck.Bind(wx.EVT_CHECKBOX, self.on_painkillercheck)

        conf_button = wx.Button(self, label='Confirm')
        conf_button.Bind(wx.EVT_BUTTON, self.on_conf)

        vis_button = wx.Button(self, label='Visualize')
        vis_button.Bind(wx.EVT_BUTTON, self.on_vis)

        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        # controlsizer=wx.BoxSizer(wx.HORIZONTAL)
        # controlsizer.Add(prev_button, proportion=1,
        #                flag=wx.ALL | wx.LEFT | wx.EXPAND,
        #                border=5)
        # controlsizer.Add(next_button, proportion=1,
        #                flag=wx.ALL | wx.RIGHT | wx.EXPAND,
        #                border=5)
        # main_sizer.Add(controlsizer, proportion=1,
        #                flag=wx.ALL | wx.CENTER | wx.EXPAND,
        #                border=5)
        main_sizer.Add(self.dateselector, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(forgotcheck, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(firstcheck, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(bloodbox, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(painbox, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(painkillercheck, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(conf_button, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(vis_button, proportion=1,
                       flag=wx.ALL | wx.LEFT | wx.SHAPED,
                       border=5)
        self.SetSizer(main_sizer)


    


    def on_selectionchanged(self, event):
        
        # date=event.PyGetDate()
        date=self.dateselector.GetDate()
        self.year=(wx.DateTime.GetYear(date))
        self.month=(wx.DateTime.GetMonth(date)+1)#!!!!!!!!!!!!!for some reason getMonth returns 0..11 instead of 1..12
        
        self.day=(wx.DateTime.GetDay(date))
        # self.day=date.day
        # self.month=date.month
        # self.year=date.year
    
    def on_pagechanged(self, event):
        self.markdays(self.dateselector)
        return
        
        
        
            

    def on_forgotcheck(self, event):
        self.forgotcheck=event.IsChecked() 
         
    

    def on_firstdaycheck(self, event):
        self.firstday=event.IsChecked()

    def on_bloodbox(self, event):
        self.blood = event.GetSelection()
    
    def on_painbox(self, event):
        self.pain=event.GetSelection()

    def on_painkillercheck(self, event):
        self.painkiller=event.IsChecked()

    def on_conf(self, event):
        if self.forgotcheck == True:
            filehandling.fillpast(savefile, self.year, self.month, self.day, 'forgotten')
        elif self.firstday == True:
            filehandling.fillpast(savefile, self.year, self.month, self.day, 'zeros')
        entryexists=filehandling.checkentryexists(savefile, self.year, self.month, self.day)
        if entryexists[0]:
            popper=wx.MessageDialog(None, 'An entry for this date already exists. Do you want to overwrite it?', 'Warning', wx.YES_NO).ShowModal()
        else:
            popper= None

        if popper == wx.ID_NO:
            return
        if popper == wx.ID_YES:
            filehandling.deleteentry(savefile,entryexists[1])
            
        print('creating entry')
        filehandling.createentry(savefile, self.year, self.month, self.day, self.firstday,self.blood, self.pain, self.painkiller, self.forgotcheck)
        filehandling.orderbydate(savefile)
        exit()    

    def on_vis(self, event):
        visualization.visualize(savefile)
        exit()
    # def on_prev(self, event):
    #     global globalcalendardate
    #     current=self.dateselector.GetDate()
    #     globalcalendardate=current.Subtract(wx.DateSpan(months=1))
    #     # globalcalendardate=current.Add(wx.DateSpan(months=1))
        
    #     globalcalendardate=date(wx.DateTime.GetYear(globalcalendardate), wx.DateTime.GetMonth(globalcalendardate)+1, wx.DateTime.GetDay(globalcalendardate))
        
    #     global quitMyAppLoop
    #     quitMyAppLoop=False
    #     # frame.Close()
    #     self.unmarkdays(self.dateselector)
        
    #     del self.dateselector
    #     frame.Destroy()
        # current=self.dateselector.GetDate()
        # previous=current.Add(wx.DateSpan(months=1))
        # # # self.dateselector.EnableMonthChange(True)
        # print(previous)
        # self.dateselector.ResetAttr(11)
        # self.dateselector.SetDate(previous)
        # # frame.Refresh()
        # sleep(0.1)
        # # self.dateselector.EnableMonthChange(False)
        # self.markdays(self.dateselector, self.markstyle)
    # def on_next(self, event):
    #     global globalcalendardate
    #     current=self.dateselector.GetDate()
    #     globalcalendardate=current.Add(wx.DateSpan(months=1))
        
    #     y=(wx.DateTime.GetYear(globalcalendardate))
    #     m=(wx.DateTime.GetMonth(globalcalendardate)+1)#!!!!!!!!!!!!!for some reason getMonth returns 0..11 instead of 1..12
        
    #     d=(wx.DateTime.GetDay(globalcalendardate))
    #     globalcalendardate=date(y,m,d)
        
    #     global quitMyAppLoop
    #     quitMyAppLoop=False
    #     # frame.Close()
    #     self.unmarkdays(self.dateselector)
        
    #     del self.dateselector
    #     frame.Destroy()
        
class MyFrame(wx.Frame):
    
    def __init__(self, calendardate):
        super().__init__(None, title='Red Calendar', size=(400, 500))
        self.panel = MyPanel(self, calendardate)
        
        self.Show()
        

import sys
import traceback

def excepthook(type, value, tb):
    message = 'Uncaught exception:\n'
    message += ''.join(traceback.format_exception(type, value, tb))
    print(message)


    
    
# def r_relaunch():
#     frame.Destroy()
#     frame=MyFrame()
#     frame.Show()

# frame=None
# app=None
# panel=None


if __name__ == '__main__':
    sys.excepthook = excepthook
    filehandling.checkcreatesavefile(savefile)
    app = wx.App(0)
    frame = MyFrame(globalcalendardate)
    app.MainLoop()
    
    
    
    
    # while quitMyAppLoop == False:
        
    #     quitMyAppLoop=True
    #     app = wx.App(0)
        
    #     frame = MyFrame(globalcalendardate)
    #     try:
    #         app.MainLoop()
    #     except:
    #         exc_info = sys.exc_info()
    #         print(exc_info)
    #     app=None
    #     frame=None
    






    