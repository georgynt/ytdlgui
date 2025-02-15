import wx
from pydantic import ValidationError

from core.urllist import UrlItem, UrlList
from gui import PosSizeMixin
from gui.settings import SettingsWindow
from gui.tasklist import TaskList
from tasks.task import TaskManager


class UrlCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetValue(">> http://youtube.com/ <<")


class MainWindow(wx.Frame, PosSizeMixin):
    window_name = 'main'

    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0)|wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.tm = TaskManager(self.on_change, self.on_change)

        self.urllist = UrlList()
        self._load()

        self.SetTitle("YouTube Downloader")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND | wx.TOP, 5)

        self.url = UrlCtrl(self, wx.ID_ANY, "")
        self.url.Bind(wx.EVT_KEY_UP, self.urlEnterKey)
        sizer_2.Add(self.url, 6, wx.LEFT, 5)

        self.btnAdd = wx.Button(self, wx.ID_ANY, "Добавить в список")
        self.btnAdd.Bind(wx.EVT_BUTTON, self.btnAddClick)
        sizer_2.Add(self.btnAdd, 1, wx.LEFT, 5)

        self.btnGo = wx.Button(self, wx.ID_ANY, "Go")
        self.btnGo.Bind(wx.EVT_BUTTON, self.btnGoClick)
        sizer_2.Add(self.btnGo, 1, wx.LEFT|wx.RIGHT, 5)

        # self.lst = UrlListCtrl(self)
        self.lst = TaskList(self)
        sizer_1.Add(self.lst, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5)

        sizer_3 = wx.GridSizer(1, 3, 0, 0)
        sizer_1.Add(sizer_3, 0, wx.ALL|wx.EXPAND, 5)

        # sizer_3.Add((0, 0), 0, 0, 0)

        self.btnClear = wx.Button(self, wx.ID_ANY, u"Очистить")
        self.btnClear.Bind(wx.EVT_BUTTON, self.btnClearClick)
        sizer_3.Add(self.btnClear, 0, 0, 5)

        self.btnGoAll = wx.Button(self, wx.ID_ANY, "GO ALL!")
        self.btnGoAll.Bind(wx.EVT_BUTTON, self.btnGoAllClick)
        sizer_3.Add(self.btnGoAll, 0, 0, 5)

        self.btnSettings = wx.Button(self, wx.ID_ANY, u"Настройки")
        self.btnSettings.Bind(wx.EVT_BUTTON, self.btnSettingsClick)
        sizer_3.Add(self.btnSettings, 0, 0, 5)

        self.SetSizer(sizer_1)
        self.Layout()

    def urlEnterKey(self, evt: wx.KeyEvent) -> None:
        if evt.KeyCode in (13, 370):
            self.btnAddClick(evt)

    def btnGoClick(self, *args, **kwargs) -> None:
        """Добавить задачу и сразу запустить"""
        self.btnAddClick(*args, **kwargs)
        self.btnGoAllClick(*args, **kwargs)

    def btnGoAllClick(self, *args, **kwargs) -> None:
        """btnGoAllClick"""
        self.tm.start()

    def on_change(self) -> None:
        self.btnGoAll.Enable(not self.tm.running)
        self.btnAdd.Enable(not self.tm.running)
        self.btnClear.Enable(not self.tm.running)
        self.btnGo.Enable(not self.tm.running)
        self.btnSettings.Enable(not self.tm.running)

    def btnSettingsClick(self, *args, **kwargs) -> None:
        """Настройки"""
        print(*args, **kwargs)
        if not hasattr(self, 'ws'):
            self.ws = SettingsWindow(self, wx.ID_ANY, "")
            self.ws.Show()
            self.Bind(wx.EVT_WINDOW_DESTROY, self.wsDestroy)

    def wsDestroy(self, *args, **kwargs) -> None:
        """close settings window"""
        if hasattr(self,'ws'):
            del self.ws

    def btnAddClick(self, *args, **kwargs) -> None:
        """Клик на кнопку ADD"""
        if len(val := self.url.GetValue()) > 0:
            try:
                urli = UrlItem(url=val)
                self.urllist.append(urli)
                self.url.Clear()
            except ValidationError as ex:
                wx.MessageBox(f"Неправильный URL для загрузки видео: \n {ex}", "Ошибка", wx.OK, self)

    def btnClearClick(self, *args, **kwargs) -> None:
        self.urllist.clear()

    def Destroy(self):
        self._save()
        return super().Destroy()
