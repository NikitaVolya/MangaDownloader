from abc import ABC, abstractmethod
from downloaders.strategies import ArchiveStrategy, DeletePicturesStrategy, \
    SavePSDStrategy, DeleteFolderStrategy, MergeFramesStrategy
from enums import DownloadMode
from entity import MangaChapter

from outils import Convertor
import os



class IMangaDownloader(ABC):

    def __init__(self):

        self._max_concurrent = 3

        self.__download_mode = DownloadMode.STANDARD
        self._strategies = []

        self.__isWorking = False

        self.OnDownloadChapterFinished = None

    @property
    def IsWorking(self):
        return self.__isWorking

    def Stop(self):
        self.__isWorking = False

    @property
    def DownloadMode(self):
        return self.__download_mode

    @DownloadMode.setter
    def DownloadMode(self, value: DownloadMode):
        assert isinstance(value, DownloadMode)
        self.__download_mode = value

        self._strategies = []

        if DownloadMode.MERGE_PICTURES in self.__download_mode:
            self._strategies.append(MergeFramesStrategy(DownloadMode.SAVE_PICTURES in self.__download_mode))

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
    def GetChapters(self, link: str) -> list[MangaChapter]:
        ...

    @abstractmethod
    def DownloadMangaPages(self, link: str, path = "download") -> list[str]:
        ...

    @abstractmethod
    def DownloadChapter(self, manga_chapter: MangaChapter, path = "download"):
        ...

    def DownloadChapters(self, link: str, path: str = "download", chapters: list[MangaChapter] = None) -> None:

        self.__isWorking = True

        link = link.split("?")[0]

        title = Convertor.ToSave(self.GetTitle(link))
        os.makedirs(f"{path}/{title}", exist_ok=True)

        if chapters is None:
            chapters: list[MangaChapter] = self.GetChapters(link)

        for chapter in chapters:
            while True:
                if not self.__isWorking:
                    break
                print("Starting chapter:", chapter.Href)
                try:
                    self.DownloadChapter(chapter, f"{path}/{title}")
                except Exception as e:
                    print("Error chapter", chapter.Href, "Error:", e)
                    print("Retrying...", chapter.Href)
                    continue
                break
            if self.OnDownloadChapterFinished:
                self.OnDownloadChapterFinished()

        self.__isWorking = False