
import requests

from entity import MangaChapter
from parsers import MangaParserInterface


class MangaRequestsDownloader:

    def __init__(self, parser: MangaParserInterface):

        self.__parser: MangaParserInterface = parser


    def GetTitle(self, link) -> str or None:
        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParseTitle(str(resp.content))

    def GetPoster(self, link):
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

    def __GetChaptersLinks(self, link) -> list[str] or None:

        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParseChaptersLinks(str(resp.content))

    def GetAllChaptersLinks(self, link) -> list[str] or None:
        chapters_links = set()
        previous_page = None
        i: int = 1
        while True:

            current_link = link + "?start=" + str(i)
            current_page = self.__GetChaptersLinks(current_link)
            if current_page is None or previous_page == current_page:
                break

            for new_chapter_link in current_page:
                chapters_links.add(new_chapter_link)

            previous_page = current_page
            i += 100

        output = list(chapters_links)
        output.sort(key=lambda tmp: tmp.split("/")[-1])

        return output

    def GetChaptersNumber(self, link) -> int:
        chapters = self.GetAllChaptersLinks(link)
        if chapters is None:
            return 0
        return len(chapters)

    def GetChapters(self, link: str) -> list[MangaChapter] or None:
        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParseChapters(str(resp.content))

    def GetAllChapters(self, link) -> list[MangaChapter] or None:
        chapters = []
        previous_chapters = None

        resp = requests.get(link)
        if resp.status_code != 200:
            return None

        i: int = 1
        while True:
            current_link = link + "?start=" + str(i)
            current_chapters = self.GetChapters(current_link)

            if current_chapters is None or previous_chapters == current_chapters:
                break

            chapters += current_chapters

            previous_chapters = current_chapters
            i += 100

        return chapters