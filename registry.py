
from MangaDownloadersContainer import MangaDownloadersContainer

from parsers import BatoToParser, XBatoParser, KaoruHanaWarinToSakuParser
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

MangaDownloadersContainer.RegisterParser(
    "Kaoru Hana Wa Rin To Saku Manga Online",
    "https://kaoruhanawarintosaku.net",
    KaoruHanaWarinToSakuParser
)