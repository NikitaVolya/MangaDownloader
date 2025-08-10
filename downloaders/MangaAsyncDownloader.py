
import os, patoolib

from outils import Convertor, MangaParser, Counter
from enums import DownloadMode

import httpx


class MangaAsyncDownloader:

    __client = httpx.AsyncClient()

    def __init__(self):

        self.__is_working = False

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
    async def __GetChaptersLinksAsync(link) -> list[str] or None:
        resp = await MangaAsyncDownloader.__client.get(link)
        if resp.status_code != 200:
            return None
        return MangaParser.ParseChaptersLinks(str(resp.content))

    @staticmethod
    async def GetAllChaptersLinksAsync(link) -> list[str] or None:
        chapters_links = set()
        previous_page = None
        i: int = 1
        while True:

            current_link = link + "?start=" + str(i)
            current_page = await MangaAsyncDownloader.__GetChaptersLinksAsync(current_link)
            if current_page is None or previous_page == current_page:
                break

            for new_chapter_link in current_page:
                chapters_links.add(new_chapter_link)

            previous_page = current_page
            i += 100

        output = list(chapters_links)
        output.sort(key=lambda link: link.split("/")[-1])

        return output

    @staticmethod
    async def GetChaptersNumber(link) -> int or None:
        chapters = await MangaAsyncDownloader.GetAllChaptersLinksAsync(link)
        if chapters is None:
            return 0
        return len(chapters)

    @staticmethod
    async def __SavePagesAsync(
            link: str,
            path: str,
            download_mode: DownloadMode,
            counter: Counter
        ) -> None:

        pagesLinks: list[str] = await MangaAsyncDownloader.__GetPagesLinksAsync(link)
        if pagesLinks is None:
            print("No pages found")
            return

        pageTitle: str = await MangaAsyncDownloader.GetTitleAsync(link)

        folderName: str = (str(counter.Value) + " - "
                           if counter is not None and DownloadMode.MARK_NUMERATION in download_mode
                           else "") + pageTitle

        files: list[str] = []

        os.makedirs(f"{path}/{folderName}", exist_ok=True)

        for i, current_link in enumerate(pagesLinks):

            resp = await MangaAsyncDownloader.__client.get(current_link)
            img_data = resp.content

            with open(f'{path}/{folderName}/{i}.jpg', 'wb') as handler:
                handler.write(img_data)
                files.append(f'{i}.jpg')

            if DownloadMode.SAVE_PSD in download_mode:
                Convertor.SavePageAsPSD(
                    f'{path}/{folderName}/{i}.jpg',
                    f'{path}/{folderName}/{i}.psd'
                )
                files.append(f'{i}.psd')


            if not DownloadMode.SAVE_PICTURES in download_mode:
                os.remove(f'{path}/{folderName}/{i}.jpg')
                files.remove(f'{i}.jpg')

        if counter:
            counter + 1

        if DownloadMode.SAVE_TO_ARCHIVE in download_mode:

            cwd = os.getcwd()
            try:
                os.chdir(f"{path}/{folderName}")
                patoolib.create_archive(
                    f"{cwd}\\{path}\\{folderName}.rar",
                    tuple(files),

                )
            finally:
                os.chdir(cwd)

        if not DownloadMode.SAVE_TO_FOLDER in download_mode:
            for f in files:
                os.remove(f'{path}/{folderName}/{f}')
            os.removedirs(f'{path}/{folderName}')
            return


    async def SaveAllChapters(
                     self,
                     link: str,
                     path: str = "download",
                     download_mode = DownloadMode.STANDARD,
                     start_counter: int = 0,
                     on_update = None
                     ) -> None:

        if self.__is_working:
            raise "Manga downloader is already working"

        self.__is_working = True

        title = await MangaAsyncDownloader.GetTitleAsync(link)
        os.makedirs(f"{path}/{title}", exist_ok=True)

        counter = Counter(start_counter)

        chapters = await MangaAsyncDownloader.GetAllChaptersLinksAsync(link)

        for chapter in chapters:

            if not self.__is_working:
                return

            current_link = "https://bato.si" + chapter
            print("Starting chapter: " + current_link)
            try:
                await MangaAsyncDownloader.__SavePagesAsync(
                    current_link,
                    f"{path}/{title}",
                    download_mode,
                    counter
                )
            except Exception as e:
                print("Error chapter", current_link, "Error:", e)

            if on_update:
                on_update()

        self.__is_working = False