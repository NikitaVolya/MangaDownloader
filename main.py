
from userInterface import MainWindow
import asyncio

from downloaders.selenium import MangaDexDownloader


async def Main():
    # window = MainWindow()
    # window.mainloop()

    href = "https://mangadex.org/title/575c6f8b-02bc-4300-b808-16e35c2bc2e2"

    downloader: MangaDexDownloader = MangaDexDownloader()
    #print(downloader.GetPosterLink(href))
    #print(downloader.GetTitle(href))
    #print(downloader.GetChapters(href))
    links = downloader.GetMangaPages("https://mangadex.org/chapter/462746f9-5fd8-4b3a-b276-0b82fa2db857")
    print(links)
    downloader.DownloadPage(links[0])


if __name__ == "__main__":
    asyncio.run(Main())