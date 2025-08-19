
class MangaChapter:

    def __init__(self, href: str, title: str):
        if not href.startswith("http"):
            href = "https://bato.si/" + href
        self.__href = href
        self.__title = title

    @property
    def Href(self) -> str:
        return self.__href

    @property
    def Title(self) -> str:
        return self.__title

    def __eq__(self, other: "MangaChapter") -> bool:
        return self.__href == other.Href

    def __str__(self):
        return f"<MangaChapter: {self.Title} - {self.Href}>"

    def __repr__(self):
        return f"<MangaChapter: {self.Title} - {self.Href}>"