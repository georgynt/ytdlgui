import wx
import wx.dataview as dv

# class VideoText(dv.DataViewTextRenderer):
class VideoText(wx.StaticText):
    def __init__(self, *args, **kwargs):
        # self.parent, *args = args
        super().__init__(*args, **kwargs)
        # super().__init__(varianttype=wx.StaticText(self.parent, wx.ID_ANY, ""), mode=dv.DATAVIEW_CELL_INERT, align=dv.DVR_DEFAULT_ALIGNMENT)
        # super().__init__(varianttype="StaticText", mode=dv.DATAVIEW_CELL_INERT, align=dv.DVR_DEFAULT_ALIGNMENT)

    # def GetParent(self) -> object:
    #     return self.parent

    def GetValue(self, *args, **kw):
        return self.GetParent()._getName()

    def GetView(self, *args, **kwargs) -> None:
        """Method Description"""
        return self.GetParent()._getName()

    def GetLabelText(self, *args, **kwargs) -> str:
        """Method Description"""
        return self.GetParent()._getName()

    def GetLabel(self, *args, **kwargs) -> str:
        """Method Description"""
        return self.GetParent()._getName()

    # def __getattribute__(self, item) -> callable:
    #     def _call(*args, **kwargs) -> object:
    #         print("CALL", args, kwargs)
    #         return object()
    #
    #     print("METHODNAME", item)
    #     return _call
