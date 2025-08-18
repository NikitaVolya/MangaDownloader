
import re
from bs4 import BeautifulSoup
from entity import MangaChapter


class MangaParser:

    @staticmethod
    def ParseTitle(content: str) -> str:

        title = re.search(r"<title q:head>(.+?)</title>", content)
        return title.group(1)

    @staticmethod
    def ParsePagesLinks(content: str) -> list[str] or None:
        mangaPages = re.findall(
            r"https://[^\s\"']+/media/[^\s\"']+\.(?:jpg|jpeg|png|gif|webp)",
            content,
            re.IGNORECASE,
        )
        return mangaPages

    @staticmethod
    def ParsePosterLink(content: str) -> str or None:
        try:
            mangaPoster = re.findall(
                r"/media/[^\s\"']+\.(?:jpg|jpeg|png|gif|webp)",
                content,
                re.IGNORECASE,
            )
            return "https://bato.si" + mangaPoster[0]
        except IndexError:
            return None

    @staticmethod
    def ParseChaptersLinks(content: str) -> list[str] or None:
        mangaChapters = re.findall(
            r"/title/[a-zA-Z\-0-9]+/\d+",
            content
        )

        return list(set(mangaChapters))

    @staticmethod
    def ParseChapters(content: str) -> list[MangaChapter] or None:

        soup = BeautifulSoup(content, "html.parser")
        chapters_list = soup.find("div", {"data-name": "chapter-list"})

        rep = []
        for chapter in chapters_list.find_all("a", {"class": "link-hover"})[::2]:
            rep.append(MangaChapter(chapter["href"], chapter.text))
        rep.reverse()
        return rep