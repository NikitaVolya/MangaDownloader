
from MangaDownloadersContainer import MangaDownloadersContainer

from parsers import BatoToParser, XBatoParser
from downloaders.selenium import MangaDexDownloader, HoneyMangaDownloader

MangaDownloadersContainer.RegisterParser(
    "BatoTo",
    "https://bato.si",
    BatoToParser
)

MangaDownloadersContainer.RegisterParser(
    "XBato",
    "https://xbato.com",
    XBatoParser
)

MangaDownloadersContainer.RegisterDownloader(
    "MangaDex",
    "https://mangadex.org",
    MangaDexDownloader
)

MangaDownloadersContainer.RegisterDownloader(
    "HoneyManga",
    "https://honey-manga.com.ua",
    HoneyMangaDownloader
)