
from parsers.MangaParserInterface import MangaParserInterface
from entity import MangaChapter

from bs4 import BeautifulSoup
import re


class KaoruHanaWarinToSakuParser(MangaParserInterface):

    @staticmethod
    def ParseTitle(content: str) -> str | None:
        return "Kaoru Hana wa Rin to Saku"

    @staticmethod
    def ParsePagesLinks(content: str) -> list[str] | None:
        mangaPages = re.findall(
            r"https://scans.lastation.us/manga/Kaoru-Hana-wa-Rin-to-Saku/[^\s\"']+\.(?:jpg|jpeg|png|gif|webp)",
            content,
            re.IGNORECASE,
        )
        return mangaPages

    @staticmethod
    def ParsePosterLink(content: str) -> str | None:
        soup = BeautifulSoup(content, "html.parser")

        poster = soup.find("img", {"class": "manga-thumb"})

        return poster.get("\\ndata-src")

    @staticmethod
    def ParseChaptersLinks(content: str) -> list[str] | None:
        soup = BeautifulSoup(content, "html.parser")

        links = soup.find_all("a", {"class": "d-block chapter-list-item"})
        res = [item.get("href") for item in links]

        return res

    @staticmethod
    def ParseChapters(content: str) -> list[MangaChapter] | None:
        soup = BeautifulSoup(content, "html.parser")

        textFilter = lambda s: s.replace("  ", "").replace("\\n", "")

        links = soup.find_all("a", {"class": "d-block chapter-list-item"})
        res = []
        for link in links:

            title = link.find("span", {"class", "chapter-name"}).text

            newChapter = MangaChapter(link.get("href"), textFilter(title))
            res.append(newChapter)

        return res
