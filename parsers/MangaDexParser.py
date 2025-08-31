from parsers import MangaParserInterface
from entity import MangaChapter
from bs4 import BeautifulSoup


class MangaDexParser(MangaParserInterface):

    @staticmethod
    def ParseTitle(content: str) -> str | None:
        return None

    @staticmethod
    def ParsePagesLinks(content: str) -> list[str] | None:
        return None

    @staticmethod
    def ParsePosterLink(content: str) -> str | None:
        soup = BeautifulSoup(content, "html.parser")

        images = soup.find_all("meta")

        for image in images:
            if image.get("property") == "og:image:secure_url":
                return image["content"]
        return None

    @staticmethod
    def ParseChaptersLinks(content: str) -> list[str] | None:
        return None

    @staticmethod
    def ParseChapters(content: str) -> list[MangaChapter] | None:
        return None