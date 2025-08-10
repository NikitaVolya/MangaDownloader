
import re

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