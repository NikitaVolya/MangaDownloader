
import requests

from outils import MangaParser

class MangaDownloader:

    @staticmethod
    def GetTitle(link) -> str or None:
        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParseTitle(str(resp.content))

    @staticmethod
    def GetPoster(link):
        try:
            resp = requests.get(link)
        except:
            return None
        if resp.status_code != 200:
            return None
        return MangaParser.ParsePosterLink(str(resp.content))

    @staticmethod
    def GetPagesLinks(link) -> list[str] or None:
        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParsePagesLinks(str(resp.content))

    @staticmethod
    def __GetChaptersLinks(link) -> list[str] or None:

        resp = requests.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParseChaptersLinks(str(resp.content))

    @staticmethod
    def GetAllChaptersLinks(link) -> list[str] or None:
        chapters_links = set()
        previous_page = None
        i: int = 1
        while True:

            current_link = link + "?start=" + str(i)
            current_page = MangaDownloader.__GetChaptersLinks(current_link)
            if current_page is None or previous_page == current_page:
                break

            for new_chapter_link in current_page:
                chapters_links.add(new_chapter_link)

            previous_page = current_page
            i += 100

        output = list(chapters_links)
        output.sort(key=lambda tmp: tmp.split("/")[-1])

        return output

    @staticmethod
    def GetChaptersNumber(link) -> int:
        chapters = MangaDownloader.GetAllChaptersLinks(link)
        if chapters is None:
            return 0
        return len(chapters)