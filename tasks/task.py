import threading
from threading import Event, Semaphore, Thread
from typing import Callable

from core.conf import Config
from core.event import Event
from core.net import youtube_download
from core.singleton import Singleton
from core.urllist import UrlItem, UrlList


class MulTask(Thread):
    url: list[UrlItem]

    def __init__(self, urls: list[UrlItem], on_change = None):
        self.urls = urls
        self.on_change = on_change
        super().__init__()

    def run(self):
        """download video task"""
        youtube_download([str(x.url) for x in self.urls], self.on_change)
        # print("start", self.urls)
        # sleep(100)
        # print("end", self.urls)



class Task(Thread):
    url: UrlItem

    def __init__(self, url: UrlItem, sem: Semaphore, on_change: Callable):
        self.url = url
        self.sem = sem
        self.on_change = on_change
        super().__init__()
        self._stop_event = Event()

    def run(self):
        """download video task"""
        youtube_download([str(self.url.url)], self.on_change)
        self.url.done = True
        self.sem.release()

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

        # thread_id = self.get_id()
        # res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
        #                                                  ctypes.py_object(SystemExit))
        # if res > 1:
        #     ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        #     print('Exception raise failure')

    def __eq__(self, obj) -> bool:
        return self.url == obj.url

    def __hash__(self):
        return hash(self.url)


class TaskManager(metaclass=Singleton):
    tasks: list[Task]
    sem: Semaphore
    max_tasks: int
    urllist: UrlList

    def __init__(self, on_start: Callable = None, on_finish: Callable = None):
        self.on_start = on_start
        self.on_finish = on_finish

        self.tasks = []
        self.urllist = UrlList()
        self.urllist.on_change += self.on_change
        self.conf = Config()
        self.max_tasks = self.conf.settings.get('parallel',5)
        self.sem = Semaphore(self.max_tasks)
        super().__init__()

    def on_change(self):
        for t in list(self.tasks):
            if t.url not in self.urllist:
                self.tasks.remove(t)
        print(self.tasks)

    def createTask(self, url: UrlItem, on_change: Callable) -> Task:
        """create task and add it to tasks"""
        t = Task(url, self.sem, on_change)
        self.addTask(t)
        return t

    def clearTasks(self):
        self.tasks.clear()

    def addTask(self, tsk: Task):
        if not tsk in self.tasks:
            self.tasks.append(tsk)

    def start(self):
        self.trd = Thread(target=self.run)
        self.trd.start()

    def run(self):
        """multiple run"""
        self.sem.acquire(True)
        if callable(self.on_start):
            self.on_start()

        for t in self.tasks:
            self.sem.acquire(True)
            t.start()

        for t in self.tasks:
            t.join()
            self.tasks.remove(t)
            # self.urllist.remove(t.url)
            self.sem.release(True)

        self.sem.release()
        if callable(self.on_finish):
            self.on_finish()


    @property
    def running(self) -> bool:
        return self.sem._value < self.max_tasks
