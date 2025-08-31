from abc import ABC, abstractmethod
from downloaders.strategies import ArchiveStrategy, DeletePicturesStrategy, \
    SavePSDStrategy, DeleteFolderStrategy, MergeFramesStrategy
from enums import DownloadMode
from entity import MangaChapter



class MangaDownloader(ABC):

    def __init__(self):

        self._max_concurrent = 3

        self.__download_mode = DownloadMode.STANDARD
        self._strategies = []

        self.OnDownloadFinished = None

    @property
    def DownloadMode(self):
        return self.__download_mode

    @DownloadMode.setter
    def DownloadMode(self, value: DownloadMode):
        assert isinstance(value, DownloadMode)
        self.__download_mode = value

        self._strategies = []

        if DownloadMode.MERGE_PICTURES in self.__download_mode:
            self._strategies.append(MergeFramesStrategy())

        if DownloadMode.SAVE_PSD in self.__download_mode:
            self._strategies.append(SavePSDStrategy())

        if not DownloadMode.SAVE_PICTURES in self.__download_mode:
            self._strategies.append(DeletePicturesStrategy())

        if DownloadMode.SAVE_TO_ARCHIVE in self.__download_mode:
            self._strategies.append(ArchiveStrategy())

        if not DownloadMode.SAVE_TO_FOLDER in self.__download_mode:
            self._strategies.append(DeleteFolderStrategy())


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
    def DownloadMangaPages(self, link: str, path = "download") -> list[str]:
        ...

    @abstractmethod
    def DownloadChapter(self, manga_chapter: MangaChapter, path = "download"):
        ...

    @abstractmethod
    def DownloadChapters(self, link: str, path: str = "download", chapters: list[MangaChapter] = None) -> None:
        ...