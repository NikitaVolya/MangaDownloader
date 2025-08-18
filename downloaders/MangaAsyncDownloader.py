
import os

from downloaders.strategies import ArchiveStrategy, DeletePicturesStrategy, SavePSDStrategy, DeleteFolderStrategy
from entity import MangaChapter
from outils import Convertor, MangaParser, Counter
from enums import DownloadMode

import httpx, asyncio


class MangaAsyncDownloader:

    __client = httpx.AsyncClient(timeout=30.0)

    def __init__(self):

        self.__is_working = False

        self.__max_concurrent = 3

        self.__download_mode = DownloadMode.STANDARD
        self.__strategies = []

        self.OnUpdate = None

    @property
    def DownloadMode(self):
        return self.__download_mode

    @DownloadMode.setter
    def DownloadMode(self, value: DownloadMode):
        assert isinstance(value, DownloadMode)
        self.__download_mode = value

        self.__strategies = []

        if DownloadMode.SAVE_PSD in self.__download_mode:
            self.__strategies.append(SavePSDStrategy())

        if not DownloadMode.SAVE_PICTURES in self.__download_mode:
            self.__strategies.append(DeletePicturesStrategy())

        if DownloadMode.SAVE_TO_ARCHIVE in self.__download_mode:
            self.__strategies.append(ArchiveStrategy())

        if not DownloadMode.SAVE_TO_FOLDER in self.__download_mode:
            self.__strategies.append(DeleteFolderStrategy())

    @property
    def IsWorking(self):
        return self.__is_working

    def Stop(self):
        self.__is_working = False

    @staticmethod
    async def GetTitleAsync(link):
        resp = await MangaAsyncDownloader.__client.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParseTitle(str(resp.content))

    @staticmethod
    async def GetPosterAsync(link):
        resp = await MangaAsyncDownloader.__client.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParsePosterLink(str(resp.content))

    @staticmethod
    async def __GetPagesLinksAsync(link) -> list[str] or None:
        resp = await MangaAsyncDownloader.__client.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParsePagesLinks(str(resp.content))

    @staticmethod
    async def GetChapters(link: str) -> list[MangaChapter] or None:
        resp = await MangaAsyncDownloader.__client.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParseChapters(str(resp.content))

    @staticmethod
    async def GetAllChapters(link) -> list[MangaChapter] or None:
        chapters = []
        previous_chapters = None

        resp = await MangaAsyncDownloader.__client.get(link)
        if resp.status_code != 200:
            return None

        i: int = 1
        while True:
            current_link = link + "?start=" + str(i)
            current_chapters = await MangaAsyncDownloader.GetChapters(current_link)

            if current_chapters is None or previous_chapters == current_chapters:
                break

            chapters += current_chapters

            previous_chapters = current_chapters
            i += 100

        return chapters

    async def SaveChapterAsync(self, chapter: MangaChapter, path: str) -> None:

        if not self.__is_working:
            return

        pagesLinks: list[str] = await MangaAsyncDownloader.__GetPagesLinksAsync(chapter.Href)
        if pagesLinks is None:
            print("No pages found")
            return

        folderName: str = Convertor.ToSave(chapter.Title)

        os.makedirs(f"{path}/{folderName}", exist_ok=True)

        for i, current_link in enumerate(pagesLinks):

            resp = await MangaAsyncDownloader.__client.get(current_link)
            img_data = resp.content

            image_path = f'{path}/{folderName}/{i + 1}.jpg'

            with open(image_path, 'wb') as handler:
                handler.write(img_data)

        for strategy in self.__strategies:
            strategy.Execute(f"{path}/{folderName}")

    async def SaveAllChapters(self, link: str, path: str = "download") -> None:

        if self.__is_working:
            raise "Manga downloader is already working"

        self.__is_working = True

        title = Convertor.ToSave(await MangaAsyncDownloader.GetTitleAsync(link))
        os.makedirs(f"{path}/{title}", exist_ok=True)

        chapters: list[MangaChapter] = await MangaAsyncDownloader.GetAllChapters(link)

        semaphore = asyncio.Semaphore(self.__max_concurrent)

        async def limited_save(chapter):
            async with semaphore:
                while True:
                    print("Starting chapter:", chapter.Href)
                    try:
                        await self.SaveChapterAsync(chapter, f"{path}/{title}")
                    except Exception as e:
                        print("Error chapter", chapter.Href, "Error:", e)
                        print("Retrying...", chapter.Href)
                        continue
                    break
                self.OnUpdate()

        tasks = [limited_save(ch) for ch in chapters]
        await asyncio.gather(*tasks)


        self.__is_working = False