import wx
from core.conf import Config


class PosSizeMixin:
    def _load(self) :
        """Загрузить параметры окна"""
        self.conf = Config()

        if not hasattr(self,'window_name'):
            self.window_name = 'main'

        wstt = self.conf.windows[self.window_name]
        self.SetSize(wx.Size(wstt['width'], wstt['height']))
        self.Move(wx.Point(wstt['left'], wstt['top']))

    def _save(self):
        """Сохранить координаты окна"""
        pos = self.GetPosition()
        sz = self.GetSize()
        x = self.conf.windows[self.window_name]
        x['left'], x['top'] = pos
        x['width'], x['height'] = sz

        self.conf.save()

