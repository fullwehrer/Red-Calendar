import wx





class MyFrame(wx.Frame):
    
    def __init__(self):
        super().__init__(None, title='Red Calendar', size=(400, 400))
        popper=wx.MessageDialog(None, 'really?', 'ABC', wx.YES_NO)
        jebedus=popper.ShowModal()
        
        self.Show()



if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = MyFrame()
    app.MainLoop()


