from downloaders.MangaRequestsDownloader import MangaRequestsDownloader
from downloaders.IMangaDownloader import IMangaDownloader
from entity import DownloaderData


class MangaDownloadersContainer:

    __downloaders: list[DownloaderData] = []

    def __init__(self):
        pass

    @staticmethod
    def GetDownloaderDataByName(value: str) -> DownloaderData | None:
        assert isinstance(value, str), "Value must by str"

        for downloaderData in MangaDownloadersContainer.__downloaders:
            if downloaderData.Name == value:
                return downloaderData
        return None

    @staticmethod
    def GetDownloaderDataByHref(value: str) -> DownloaderData | None:
        assert isinstance(value, str), "Value must by str"

        for downloaderData in MangaDownloadersContainer.__downloaders:
            if downloaderData == value:
                return downloaderData
        return None

    @staticmethod
    def GetDownloaderByName(value: str) -> IMangaDownloader | None:
        downloaderData = MangaDownloadersContainer.GetDownloaderDataByName(value)
        return None if downloaderData is None else downloaderData.DownloaderConstructor

    @staticmethod
    def GetDownloaderByHref(value: str) -> IMangaDownloader | None:
        downloaderData = MangaDownloadersContainer.GetDownloaderDataByHref(value)
        return None if downloaderData is None else downloaderData.DownloaderConstructor

    @staticmethod
    def RegisterDownloader(
            name: str,
            href: str,
            downloader_constructor
    ):
        assert MangaDownloadersContainer.GetDownloaderByName(name) is None, "Downloader with same name already exist"
        assert MangaDownloadersContainer.GetDownloaderDataByHref(href) is None, "Downloader with same href already exist"

        newDownloaderData = DownloaderData(name, href, downloader_constructor)
        MangaDownloadersContainer.__downloaders.append(newDownloaderData)

    @staticmethod
    def RegisterParser(
            name: str,
            href: str,
            parser_constructor
    ):
        assert MangaDownloadersContainer.GetDownloaderByName(name) is None, "Downloader with same name already exist"
        assert MangaDownloadersContainer.GetDownloaderDataByHref(href) is None, "Downloader with same href already exist"

        newDownloaderData = DownloaderData(name, href, lambda : MangaRequestsDownloader(parser_constructor()))
        MangaDownloadersContainer.__downloaders.append(newDownloaderData)

    @staticmethod
    def DownloaderDataList():
        return [data for data in MangaDownloadersContainer.__downloaders]