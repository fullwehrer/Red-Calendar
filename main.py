#GUI Tutorial used: https://www.blog.pythonlibrary.org/2021/09/29/create-gui/
# solution to calendar SetAttr() related Problem: https://discuss.wxpython.org/t/wx-adv-genericcalendarctrl-crashes-the-frame-when-using-setattr/36096


from time import sleep
import wx
import wx.adv
from datetime import datetime, date


# print(wx.version())

import filehandling
import visualization



global savefile 
savefile ='redcalendar.csv'
global showperiodchart
showperiodchart=False
now=datetime.today()


def getmonthentries(month):
    pastentries=filehandling.getpastentries(savefile)
    pastentries = [row for row in pastentries if row[1]==month]
    result= [row[2] for row in pastentries]
    return(result)


class MyPanel(wx.Panel):

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
            
            for daytomark in monthentrylist:
                if True:
                    markstyle=wx.adv.CalendarDateAttr(colBack='green')
                    dateselector.SetAttr(daytomark,markstyle)
            self.Show()
                

    def __init__(self, parent):
        super().__init__(parent)
        
        today=datetime.today()
        self.year = today.year
        self.month = today.month
        self.day = today.day
        

        self.firstday=False
        self.blood = 0
        self.pain = 0
        self.painkiller = False
        self.forgotcheck=False

        self.dateselector=wx.adv.GenericCalendarCtrl(self, name="datectrl", date=today)
        self.dateselector.EnableHolidayDisplay(False)
        self.dateselector.EnableMonthChange(True)
        self.dateselector.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,self.on_selectionchanged)
        self.markdays(self.dateselector)
        self.dateselector.Bind(wx.adv.EVT_CALENDAR_PAGE_CHANGED,self.on_pagechanged)

        forgotcheck=wx.CheckBox(self, label="FORGOTTEN? - first entry since longer, forgot to enter last bleeding/pain? (all days from last entry will be marked forgotten)",
            name='forgot_check_box')
        forgotcheck.Bind(wx.EVT_CHECKBOX, self.on_forgotcheck)

        firstcheck=wx.CheckBox(self, label="no pain/bleeding since last entry? (all days from last entry will be marked pain/bloodfree unless FORGOTTEN is also checked)",
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
        
        date=self.dateselector.GetDate()
        self.year=(wx.DateTime.GetYear(date))
        self.month=(wx.DateTime.GetMonth(date)+1)#!!!!!!!!!!!!!for some reason getMonth returns 0..11 instead of 1..12
        self.day=(wx.DateTime.GetDay(date))
    
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
        global showperiodchart
        showperiodchart = True
        destroyframe()
        
def destroyframe():
    frame.Destroy()
        
class MyFrame(wx.Frame):
    
    def __init__(self):
        super().__init__(None, title='Red Calendar', size=(400, 500))
        self.panel = MyPanel(self)
        
        self.Show()
        


frame=None
if __name__ == '__main__':
    filehandling.checkcreatesavefile(savefile)
    app = wx.App(0)
    frame = MyFrame()
    app.MainLoop()
    if showperiodchart:
        visualization.visualize(savefile)

    

