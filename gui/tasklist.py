import wx

from core.urllist import UrlItem, UrlList
from gui.controls import VideoText
from tasks.task import MulTask, Task, TaskManager

PROGRESS_COEF = 100

LBL_WAIT = 'Ожидание..'
LBL_DELETE = 'Убрать'
LBL_STOP = 'Стоп'


class TaskRow(wx.Panel):
    def __init__(self, parent, url: UrlItem):
        super().__init__(parent, wx.ID_ANY)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.url = url

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 10, wx.ALL, 5)

        self.lblVideo = VideoText(self, wx.ID_ANY, "")
        sizer_2.Add(self.lblVideo, 0, 0, 0)

        self.progress = wx.Gauge(self, wx.ID_ANY, PROGRESS_COEF)
        sizer_2.Add(self.progress, 0, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        self.lblIndicator = wx.StaticText(self, wx.ID_ANY, LBL_WAIT, style=wx.ALIGN_CENTER_HORIZONTAL)
        sizer_3.Add(self.lblIndicator, 0, wx.ALL | wx.EXPAND, 5)

        self.btnDel = wx.Button(self, wx.ID_ANY, LBL_DELETE)
        self.btnDel.Bind(wx.EVT_BUTTON, self.btnDelClick)
        sizer_3.Add(self.btnDel, 0, wx.ALL, 5)

        self.SetSizer(sizer_1)

        self.Layout()

        # print(self.url)
        tm = TaskManager()
        self.task = tm.createTask(self.url, self.on_change)
        self.setVideoName(str(self.url.name))

    def on_change(self, data) -> None:
        dl = data.get('downloaded_bytes',0)
        if not (tb := data.get('total_bytes')):
            dl = data.get('fragment_index', 0)
            tb = data.get('fragment_count', 1)
        v = int(dl/tb * PROGRESS_COEF)

        if v <= self.progress.Range:
            self.progress.SetValue(v)

        self.stt = data.get('status', LBL_WAIT)
        if self.stt != self.lblIndicator.GetLabel():
            self.lblIndicator.SetLabelText(self.stt)

        self.url.name = data.get('filename')
        self.lblVideo.SetLabelText(self.url.name)
        if self.need_stop:
            self.lblIndicator.SetLabelText("ПРЕРВАНО!")
            self.stt = "ПРЕРВАНО!"
            raise Exception()
        # self.Layout()

    @property
    def need_stop(self) -> bool:
        return getattr(self,'_need_stop',False)

    @need_stop.setter
    def need_stop(self, value: bool):
        self._need_stop = value

    def setVideoName(self, name: str):
        print(name)
        self.lblVideo.SetLabelText(name)

    def btnDelClick(self, evt):
        if hasattr(self,'stt') and ('download' in self.stt or 'ПРЕР' in self.stt):
            self.need_stop = True
        else:
            self.url.selfDelete()

    def _getName(self) -> str:
        return self.url.name


class TaskList(wx.Panel):
    urllist: UrlList

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, wx.ID_ANY, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.urllist = UrlList()
        self.urllist.on_change += self._refresh_items
        self.Layout()
        # end wxGlade

    def _refresh_items(self):
        self.sizer.Clear(True)
        for url in self.urllist:
            tr = TaskRow(self, url)
            self.sizer.Add(tr, 0, wx.ALL|wx.EXPAND, 5)
        self.Layout()
