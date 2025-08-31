from abc import ABC, abstractmethod

class MangaDownloader(ABC):

    @abstractmethod
    def GetPosterLink(self, link: str) -> str | None:
        ...

    @abstractmethod
    def GetTitle(self, link: str) -> str | None:
        ...

    @abstractmethod
    def GetChapters(self, link: str) -> list[str]:
        ...

    @abstractmethod
    def GetMangaPages(self, link: str) -> list[str]:
        ...