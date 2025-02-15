import wx

from core.conf import Config
from gui import PosSizeMixin


class SettingsWindow(wx.Frame, PosSizeMixin):
    window_name = 'settings'

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        # kwds["style"] = kwds.get("style", 0)|wx.DEFAULT_FRAME_STYLE|wx.CLIP_CHILDREN
        kwds["style"] = (kwds.get("style",0)|wx.CLIP_CHILDREN|wx.STAY_ON_TOP|wx.DEFAULT_FRAME_STYLE)
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("Settings")
        self._load()

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, "Proxy")
        sizer_1.Add(label_1, 0, wx.LEFT | wx.TOP, 5)

        self.proxy_ctrl = wx.TextCtrl(self, wx.ID_ANY, "")
        self.proxy_ctrl.SetLabelText("Proxy")
        sizer_1.Add(self.proxy_ctrl, 0, wx.ALL|wx.EXPAND, 5)

        label_2 = wx.StaticText(self, wx.ID_ANY, "Parallels")
        sizer_1.Add(label_2, 0, wx.LEFT | wx.TOP, 5)

        self.parallel_ctrl = wx.SpinCtrl(self, wx.ID_ANY, "5", min=0, max=100)
        self.parallel_ctrl.SetLabelText("Parallels")
        sizer_1.Add(self.parallel_ctrl, 0, wx.ALL|wx.EXPAND, 5)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)

        grid_sizer_1 = wx.GridSizer(1, 5, 0, 0)
        sizer_1.Add(grid_sizer_1, 0, wx.ALL | wx.EXPAND, 5)

        grid_sizer_1.Add((0, 0), 0, 0, 0)

        grid_sizer_1.Add((0, 0), 0, 0, 0)

        grid_sizer_1.Add((0, 0), 0, 0, 0)

        self.btnSave = wx.Button(self, wx.ID_ANY, "Save")
        self.btnSave.Bind(wx.EVT_BUTTON, self.btnSaveClick)
        grid_sizer_1.Add(self.btnSave, 0, 0, 0)

        self.btnCancel = wx.Button(self, wx.ID_ANY, "Cancel")
        self.btnCancel.Bind(wx.EVT_BUTTON, self.btnCancelClick)
        grid_sizer_1.Add(self.btnCancel, 0, 0, 0)

        self.SetSizer(sizer_1)

        self.Layout()
        self.proxy_ctrl.SetValue(self.conf.settings.get('proxy') or "")
        self.parallel_ctrl.SetValue(self.conf.settings.get('parallel') or 0)
        # end wxGlade

    def btnSaveClick(self, *args, **kwargs) -> None:
        """Save"""
        conf = Config()
        conf.settings['proxy'] = self.proxy_ctrl.GetValue()
        conf.settings['parallel'] = self.parallel_ctrl.GetValue()
        conf.save()
        self.btnCancelClick(*args, **kwargs)

    def btnCancelClick(self, *args, **kwargs) -> None:
        """Method Description"""
        self.Close()
        self.Destroy()
