
from MangaDownloadersContainer import MangaDownloadersContainer

from parsers import BatoToParser, XBatoParser
from downloaders.selenium import MangaDexDownloader

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