
import os

from downloaders.strategies import ArchiveStrategy, DeletePicturesStrategy, SavePSDStrategy, DeleteFolderStrategy
from entity import MangaChapter
from parsers import MangaParserInterface
from outils import Convertor
from enums import DownloadMode

import httpx, asyncio


class MangaRequestsAsyncDownloader:

    def __init__(self, parser: MangaParserInterface):

        self.__client = httpx.AsyncClient(timeout=30.0)

        self.__is_working = False

        self.__parser: MangaParserInterface = parser

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

    async def GetTitleAsync(self, link):
        resp = await self.__client.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParseTitle(str(resp.content))

    async def GetPosterAsync(self, link):
        resp = await self.__client.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParsePosterLink(str(resp.content))

    async def __GetPagesLinksAsync(self, link) -> list[str] or None:
        resp = await self.__client.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParsePagesLinks(str(resp.content))

    async def GetChapters(self, link: str) -> list[MangaChapter] or None:
        resp = await self.__client.get(link)
        if resp.status_code != 200:
            return None
        return self.__parser.ParseChapters(str(resp.content))

    async def GetAllChapters(self, link) -> list[MangaChapter] or None:
        chapters = []
        previous_chapters = None

        resp = await self.__client.get(link)
        if resp.status_code != 200:
            return None

        i: int = 1
        while True:
            current_link = link + "?start=" + str(i)
            current_chapters = await self.GetChapters(current_link)

            if current_chapters is None or previous_chapters == current_chapters:
                break

            chapters += current_chapters

            previous_chapters = current_chapters
            i += 100

        return chapters

    async def SaveChapterAsync(self, chapter: MangaChapter, path: str) -> None:

        if not self.__is_working:
            return

        pagesLinks: list[str] = await self.__GetPagesLinksAsync(chapter.Href)
        if pagesLinks is None:
            print("No pages found")
            return

        folderName: str = Convertor.ToSave(chapter.Title)

        os.makedirs(f"{path}/{folderName}", exist_ok=True)

        for i, current_link in enumerate(pagesLinks):

            resp = await self.__client.get(current_link)
            img_data = resp.content

            image_path = f'{path}/{folderName}/{i + 1}.jpg'

            with open(image_path, 'wb') as handler:
                handler.write(img_data)

        for strategy in self.__strategies:
            strategy.Execute(f"{path}/{folderName}")

    async def SaveChapters(self, link: str, path: str = "download", chapters: list[MangaChapter] = None) -> None:

        if self.__is_working:
            raise "Manga downloader is already working"

        self.__is_working = True

        title = Convertor.ToSave(await self.GetTitleAsync(link))
        os.makedirs(f"{path}/{title}", exist_ok=True)

        if chapters is None:
            chapters: list[MangaChapter] = await self.GetAllChapters(link)

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