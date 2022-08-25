from datetime import datetime
import wx
date=wx.DateTime(5,1,2022)
a=wx.DateTime.GetLastMonthDay(date)
print(a)
print(wx.DateTime.GetDay(a))