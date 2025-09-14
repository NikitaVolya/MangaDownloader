from argparse import ArgumentTypeError

from downloaders import IMangaDownloader


class DownloaderData:

    def __init__(self, name: str, href: str, downloader_constructor: IMangaDownloader):

        self.__name = name
        self.__href = href.lower()
        self.__downloader_constructor = downloader_constructor

    @property
    def Name(self) -> str:
        return self.__name

    @property
    def Href(self) -> str:
        return self.__href

    @property
    def DownloaderConstructor(self):
        return self.__downloader_constructor

    def __eq__(self, other: 'str | DownloaderData'):
        if isinstance(other, str):
            return other.lower().startswith(self.__href)
        elif isinstance(other, DownloaderData):
            return self.__name == other.Name and self.__href == other.Href
        raise ArgumentTypeError("DownloaderData == other : other must be str or Downloader Data")