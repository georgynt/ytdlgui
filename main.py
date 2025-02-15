# from wx import wx
import wx

from gui.mainwin import MainWindow


class YTDLApp(wx.App):
    def OnInit(self):
        self.mwnd = MainWindow(None, wx.ID_ANY, "")
        self.SetTopWindow(self.mwnd)
        self.mwnd.Show()

        return True

    def Exit(self) -> None:
        pass


if __name__ == '__main__':
    app = YTDLApp()
    app.MainLoop()
