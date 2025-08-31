from entity import MangaChapter
from userInterface import MainWindow
from enums import DownloadMode
import asyncio

from downloaders import MangaDexDownloader


async def Main():
    # window = MainWindow()
    # window.mainloop()

    href = "https://mangadex.org/title/575c6f8b-02bc-4300-b808-16e35c2bc2e2"

    downloader: MangaDexDownloader = MangaDexDownloader()
    downloader.DownloadMode = DownloadMode.MERGE_PICTURES | DownloadMode.SAVE_TO_FOLDER

    chapters = downloader.GetChapters(href)
    downloader.DownloadChapters(href, chapters=[chapters[8]])


if __name__ == "__main__":
    asyncio.run(Main())