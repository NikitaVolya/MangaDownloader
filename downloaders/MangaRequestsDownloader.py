
import requests

from entity import MangaChapter
from parsers import MangaParserInterface

from downloaders.IMangaDownloader import IMangaDownloader
from outils import Convertor
import os


class MangaRequestsDownloader(IMangaDownloader):

    def __init__(self, parser: MangaParserInterface):
        super().__init__()
        self.__parser: MangaParserInterface = parser


    def GetTitle(self, link: str) -> str | None:
        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParseTitle(str(resp.content))

    def GetPosterLink(self, link: str) -> str | None:
        try:
            resp = requests.get(link)
        except:
            return None
        if resp.status_code != 200:
            return None
        return self.__parser.ParsePosterLink(str(resp.content))

    def GetPagesLinks(self, link) -> list[str] or None:
        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParsePagesLinks(str(resp.content))

    def __GetPageChapters(self, link: str) -> list[MangaChapter] or None:
        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParseChapters(str(resp.content))

    def GetChapters(self, link) -> list[MangaChapter] or None:
        chapters = []
        previous_chapters = None

        resp = requests.get(link)
        if resp.status_code != 200:
            return None

        i: int = 1
        while True:
            current_link = link + "?start=" + str(i)
            current_chapters = self.__GetPageChapters(current_link)

            if current_chapters is None or previous_chapters == current_chapters:
                break

            chapters += current_chapters

            previous_chapters = current_chapters
            i += 100

        return chapters

    def DownloadMangaPages(self, link: str, path = "download") -> list[str]:
        resp = requests.get(link)
        if resp.status_code != 200:
            return []

        pages = self.__parser.ParsePagesLinks(str(resp.content))

        rep = []
        for i, page_href in enumerate(pages):

            image_path = f"{path}/{i + 1}.jpg"

            page = requests.get(page_href)
            if page.status_code != 200:
                return []

            with open(image_path, "wb") as f:
                f.write(page.content)

            rep.append(image_path)

        return rep

    def DownloadChapter(self, manga_chapter: MangaChapter, path = "download"):

        chapter_path = f"{path}/{Convertor.ToSave(manga_chapter.Title)}"
        os.makedirs(chapter_path, exist_ok=True)
        self.DownloadMangaPages(manga_chapter.Href, chapter_path)

        for strategy in self._strategies:
            strategy.Execute(chapter_path)