from abc import ABC, abstractmethod
from entity import MangaChapter


class MangaParserInterface(ABC):

    @staticmethod
    @abstractmethod
    def ParseTitle(content: str) -> str | None:
        ...

    @staticmethod
    @abstractmethod
    def ParsePagesLinks(content: str) -> list[str] | None:
        ...

    @staticmethod
    @abstractmethod
    def ParsePosterLink(content: str) -> str | None:
        ...

    @staticmethod
    @abstractmethod
    def ParseChaptersLinks(content: str) -> list[str] | None:
        ...

    @staticmethod
    @abstractmethod
    def ParseChapters(content: str) -> list[MangaChapter] | None:
        ...