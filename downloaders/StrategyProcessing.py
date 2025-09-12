from multiprocessing import Queue, Process, Value, Lock, Event, cpu_count
from threading import Thread
from downloaders.strategies import DownloadStrategy


def process_worker(queue: Queue, updateEvent: Event):
    while True:
        item = queue.get()
        if item is None:
            break

        strategies, path = item
        for strategy in strategies:
            strategy.Execute(path)

        updateEvent.set()
        updateEvent.clear()


class StrategyProcessing:

    def __init__(self, workers: int = 2):
        self.__queue = Queue()
        self.__lock = Lock()
        self.__updateEvent = Event()
        self.__isWork = Value("b", False)
        self.__workers = workers
        self.__processes: list[Process] = []

    def AddStrategy(self, strategies: list[DownloadStrategy], path: str):
        self.__queue.put([strategies, path])

    def Stop(self):
        for _ in range(self.__workers):
            self.__queue.put(None)

    def IsWork(self):
        return self.__isWork.value

    def Start(self, on_update=None):
        if self.IsWork():
            return

        self.__isWork.value = True
        self.__processes.clear()

        for _ in range(self.__workers):
            p = Process(target=process_worker, args=(self.__queue, self.__updateEvent))
            p.start()
            self.__processes.append(p)

        def updateWatcher():
            while any(p.is_alive() for p in self.__processes):
                if self.__updateEvent.wait(0.1):
                    if on_update:
                        on_update()
            self.__isWork.value = False

        if on_update is not None:
            Thread(target=updateWatcher, daemon=True).start()
