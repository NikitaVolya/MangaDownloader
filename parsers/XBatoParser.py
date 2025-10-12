
from parsers.MangaParserInterface import MangaParserInterface
from entity import MangaChapter

from bs4 import BeautifulSoup
import re


class XBatoParser(MangaParserInterface):

    @staticmethod
    def ParseTitle(content: str) -> str | None:

        soup = BeautifulSoup(content, "html.parser")
        titleWrapper = soup.find("h3", {"class": "text-lg"})
        if titleWrapper is None:
            return None

        titleElement = titleWrapper.find("a")
        if titleElement is None:
            return None

        title = re.sub(r'\\x[\w\W\d]{2}','', titleElement.text)
        return title

    @staticmethod
    def ParsePagesLinks(content: str) -> list[str] | None:
        rep = []
        mangaPages = re.findall(
            r"https://[^\s\"']+/media/[^\s\"']+\.(?:jpg|jpeg|png|gif|webp)",
            content,
            re.IGNORECASE,
        )
        for item in mangaPages:
            rep += item.replace("\\\\&quot;", "").replace("[0,", "").split("],")
        return rep

    @staticmethod
    def ParsePosterLink(content: str) -> str | None:
        soup = BeautifulSoup(content, "html.parser")
        poster = soup.find("img", {"class": "w-full not-prose shadow-md shadow-black/50"})
        return poster.get("src") if not poster is None else None

    @staticmethod
    def ParseChaptersLinks(content: str) -> list[str] | None:
        soup = BeautifulSoup(content, "html.parser")

        chaptersList = soup.find_all("astro-slot")
        if chaptersList is None:
            return None

        chapters = chaptersList[1].find_all("a", {"class": "visited:text-accent"})

        return ["https://xbato.com" + chapter.get("href") + "?=load=2" for chapter in chapters]

    @staticmethod
    def ParseChapters(content: str) -> list[MangaChapter] | None:

        soup = BeautifulSoup(content, "html.parser")

        chaptersList = soup.find_all("astro-slot")
        if chaptersList is None:
            return None

        chapters = chaptersList[1].find_all("a", {"class": "visited:text-accent"})

        textFilter = lambda s: s.replace("  ", "").replace("\\n", "")

        return [MangaChapter("https://xbato.com" + chapter.get("href") + "?=load=2", textFilter(chapter.text)) for chapter in chapters]