from tkinter import *

from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style

import requests

from downloaders.IMangaDownloader import IMangaDownloader

from registry import MangaDownloadersContainer

from userInterface.Setup import ENTRY_STYLE, BTN_STYLE, LABEL_STYLE, CHK_STYLE, APP_BACKGROUND
from userInterface.ChaptersList import ChaptersList
from enums import DownloadMode

from threading import Thread


class DownloadChaptersFrame(Frame):

    class DownloadOption:

        def __init__(self, master: "DownloadChaptersFrame", title: str, mode: DownloadMode):
            self.__master = master
            self.__booleanValue = BooleanVar()
            self.__title = title
            self.__mode = mode

            self.__checkButton = None

        def packTkinterElement(self, is_selected: bool = False):
            self.__checkButton = Checkbutton(
                self.__master,
                text=self.__title,
                **CHK_STYLE,
                variable=self.__booleanValue
            )
            if is_selected:
                self.__checkButton.select()
            self.__checkButton.pack(anchor="w", padx=10, pady=2)

        @property
        def DownloadMode(self) -> DownloadMode:
            return self.__mode

        @property
        def Title(self) -> str:
            return self.__title

        @property
        def Selected(self) -> bool:
            return self.__booleanValue.get()


    def __init__(self, master):
        super().__init__(master, bg=APP_BACKGROUND)

        self.master = master

        style = Style()
        style.theme_use("clam")

        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#1e1e1e",
            background="#007acc",
            bordercolor="#1e1e1e",
            lightcolor="#007acc",
            darkcolor="#007acc",
            thickness=20
        )

        Label(self, text="Link to main page of manga", **LABEL_STYLE).pack()

        self.__linkValue = StringVar()
        self.__linkEntry = Entry(self, **ENTRY_STYLE, textvariable=self.__linkValue)
        self.__linkEntry.pack(fill=X, padx=10, pady=5)

        self.__loadManga = Button(self, text="Load Manga", **BTN_STYLE, command=lambda : self.__OnLinkChange())
        self.__loadManga.pack(fill=X, padx=10, pady=5)

        self.__savePath = StringVar()
        self.__savePath.set("download")

        self.__selectPath = Button(self, text="Select path", **BTN_STYLE, command=lambda: self.__choseDirectory())
        self.__selectPath.pack(fill=X, padx=10, pady=5)

        self.__chaptersList = ChaptersList(self)

        self.__downloadOptions: list[DownloadChaptersFrame.DownloadOption] = []
        downloadOptions = [
            ("Save to folder", DownloadMode.SAVE_TO_FOLDER, True),
            ("Save to archive", DownloadMode.SAVE_TO_ARCHIVE, False),
            ("Save with pictures", DownloadMode.SAVE_PICTURES, True),
            ("Save PSD", DownloadMode.SAVE_PSD, False),
            ("Save PDF", DownloadMode.SAVE_PDF, False),
            ("Merge frames", DownloadMode.MERGE_PICTURES, False)
        ]
        for text, command, is_selected in downloadOptions:
            option = self.DownloadOption(self, text, command)
            self.__downloadOptions.append(option)
            option.packTkinterElement(is_selected)

        self.__downloadBtn = Button(self, text="Download", **BTN_STYLE, command=lambda: self.__OnDownloadClick())
        self.__downloadBtn.pack(fill=X, padx=10, pady=5)

        self.__progress = IntVar()
        self.__progressBar = Progressbar(self, length=100, style="Custom.Horizontal.TProgressbar", variable=self.__progress)
        self.__progressBar.pack(fill=X, padx=10, pady=5)

        self.__mangaDownloader: IMangaDownloader = None

    def __OnLinkChange(self):

        manga_link: str = self.__linkEntry.get()

        downloaderData = MangaDownloadersContainer.GetDownloaderDataByHref(manga_link)
        if downloaderData is None:
            messagebox.showerror("Error", "Invalid site")
            return

        self.__mangaDownloader = downloaderData.DownloaderConstructor()

        poster_link = self.__mangaDownloader.GetPosterLink(manga_link)
        if poster_link is None:
            return

        self.master.poster.LoadPoster(poster_link)
        self.__chaptersList.LoadChapters(self.__mangaDownloader, manga_link)


    def __StartDownload(self):
        self.__mangaDownloader.DownloadChapters(
                link=self.__linkValue.get(),
                path=self.__savePath.get(),
                chapters=self.__chaptersList.SelectedChapters
            )

    def __OnDownloadClick(self):

        if self.__mangaDownloader.IsWorking:
            return

        print("Downloading...")

        link = self.__linkValue.get()
        try:
            requests.get(link)
        except:
            print("Aborting...")
            messagebox.showerror("Error", f"Could not download from {link}")
            return

        selectedChapters = self.__chaptersList.SelectedChapters
        if selectedChapters is None:
            print("Aborting...")
            messagebox.showerror("Error", "Chapters are not selected")
            return

        download_mode = DownloadMode.NULL

        for option in self.__downloadOptions:
            if option.Selected:
                download_mode |= option.DownloadMode

        if not (DownloadMode.SAVE_TO_FOLDER in download_mode or
                DownloadMode.SAVE_TO_ARCHIVE in download_mode):
            print("Aborting...")
            messagebox.showerror("Error", "Please select a folder or archive saving mode")
            return

        if not (DownloadMode.SAVE_PICTURES in download_mode or
                DownloadMode.SAVE_PSD in download_mode or
                DownloadMode.SAVE_PDF in download_mode):
            print("Aborting...")
            messagebox.showerror("Error", "Please select a pictures or PSD saving mode")
            return

        self.__mangaDownloader.DownloadMode = download_mode
        self.__downloadBtn['text'] = "Downloading..."

        download_counter_end = len(selectedChapters)

        def on_update():

            self.__progressBar.step(100.0 / download_counter_end)

            if self.__progress.get() == 0:
                self.__downloadBtn['text'] = "Download"
                messagebox.showinfo("Download Complete", "Download Complete")

        self.__mangaDownloader.OnDownloadChapterFinished = on_update

        downloadThread = Thread(target=self.__StartDownload)
        downloadThread.start()


    def __choseDirectory(self):
        folder_path = filedialog.askdirectory(title="Оберіть папку для збереження")
        if folder_path:
            self.__savePath.set(folder_path)
