from Cython.Compiler.Errors import reset

from parsers import MangaParserInterface
from entity import MangaChapter

from bs4 import BeautifulSoup
import re


class XBatoParser(MangaParserInterface):

    @staticmethod
    def ParseTitle(content: str) -> str | None:

        soup = BeautifulSoup(content, "html.parser")
        titleWrapper = soup.find("h3", {"class": "item-title"})
        if titleWrapper is None:
            return None

        titleElement = titleWrapper.find("a")
        if titleElement is None:
            return None

        title = re.sub(r'\\x[\w\W\d]{2}','', titleElement.text)
        return title

    @staticmethod
    def ParsePagesLinks(content: str) -> list[str] | None:

        imagesListe = re.findall(r"const imgHttps = \[(\"[\w\W\d/:]*\")*]", content)
        if len(imagesListe) == 0:
            return None
        pages = imagesListe[0].replace('"', '').split(",")
        return pages

    @staticmethod
    def ParsePosterLink(content: str) -> str | None:
        soup = BeautifulSoup(content, "html.parser")
        posterWrapper = soup.find("div", {"class": "attr-cover"})
        if posterWrapper is None:
            return None

        poster = posterWrapper.find("img")
        return poster.get("src") if not poster is None else None

    @staticmethod
    def ParseChaptersLinks(content: str) -> list[str] | None:
        soup = BeautifulSoup(content, "html.parser")

        chaptersList = soup.find("div", {"class": "episode-list"})
        if chaptersList is None:
            return None

        chapters = chaptersList.find_all("a", {"class": "chapt"})

        return ["https://xbato.com" + chapter.get("href") for chapter in chapters]

    @staticmethod
    def ParseChapters(content: str) -> list[MangaChapter] | None:

        soup = BeautifulSoup(content, "html.parser")

        chaptersList = soup.find("div", {"class": "episode-list"})
        if chaptersList is None:
            return None

        chapters = chaptersList.find_all("a", {"class": "chapt"})

        textFilter = lambda s: s.replace("  ", "").replace("\\n", "")

        return [MangaChapter("https://xbato.com" + chapter.get("href"), textFilter(chapter.text)) for chapter in chapters]