from pydantic import BaseModel, HttpUrl

from core.event import Event
from core.singleton import Singleton
# from events import Events

class UrlItem(BaseModel):
    __parent = None
    _name: str|None = None
    url: HttpUrl
    done: bool = False

    def __eq__(self, obj) -> bool:
        return self.url == obj.url

    def __hash__(self):
        return hash(self.url)

    @property
    def name(self) -> str:
        # return getattr(self,'__name',str(self.url))
        return self._name or str(self.url)

    @name.setter
    def name(self, value: str):
        self._name = value

    def setParent(self, parent):
        self.__parent = parent

    def selfDelete(self):
        self.__parent.remove(self)


_UrlList = list[UrlItem]

class UrlList(_UrlList, metaclass=Singleton):
    on_change = Event()

    def __iter__(self):
        return super().__iter__()

    def __init__(self, on_change=None):
        super().__init__()
        self.on_change = on_change

    def append(self, item: UrlItem) -> None:
        """append item"""
        if not item in self:
            item.setParent(self)
            super().append(item)
            self.on_change()

    def remove(self, item: UrlItem) -> None:
        """remove item"""
        index = self.index(item)
        super().remove(item)
        self.on_change()

    def clear(self):
        print(self)
        super().clear()
        self.on_change()

    def setCtrl(self, ctrl):
        pass

