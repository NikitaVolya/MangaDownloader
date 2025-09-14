
from entity import MangaChapter
from downloaders.IMangaDownloader import IMangaDownloader

from tkinter.ttk import Treeview
from tkinter import END

from threading import Thread


class ChaptersList:

    def __init__(self, master):

        self.__chapters: list[MangaChapter] = []

        self.__tree = Treeview(master, columns=["Chapter"], show="headings", selectmode="extended",
                               style="Custom.Treeview")

        self.__tree.heading("Chapter", text="Chapters")
        self.__tree.column("Chapter", width=300)
        self.__tree.pack(expand=True)


    def Clear(self):
        self.__chapters = []
        self.__tree.delete(*self.__tree.get_children())

    def LoadChapters(self, downloader: IMangaDownloader, link: str):
        def worker():
            self.Clear()
            chapters = downloader.GetChapters(link)
            for chapter in chapters:
                self.AddChapter(chapter)

        Thread(target=worker).start()

    def AddChapter(self, chapter: MangaChapter):
        self.__tree.insert('', END, iid=str(len(self.__chapters)), values=(chapter.Title,))
        self.__chapters.append(chapter)

    @property
    def SelectedChapters(self) -> list[MangaChapter] | None:
        selection = self.__tree.selection()
        result = [self.__chapters[int(iid)] for iid in selection]
        return result if len(result) > 0 else None

