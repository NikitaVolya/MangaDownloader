
from abc import ABC, abstractmethod

class DownloadStrategy(ABC):

    @abstractmethod
    def Execute(self, path: str):
        pass