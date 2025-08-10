from tkinter import *

from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style

import requests, httpx, asyncio

from downloaders import MangaDownloader, MangaAsyncDownloader
from userInterface.Setup import ENTRY_STYLE, BTN_STYLE, LABEL_STYLE, CHK_STYLE
from enums import DownloadMode

from threading import Thread


class DownloadChaptersFrame(Frame):

    def __init__(self, master: "MainWindow"):
        super().__init__(master, bg="#1e1e1e")

        self.master: "MainWindow" = master

        self.__linkValue = StringVar()
        self.__linkValue.trace_add("write", (lambda a, b, c: self.__OnLinkChange()))

        self.__savePath = StringVar()
        self.__savePath.set("download")

        Label(self, text="Link to main page of manga", **LABEL_STYLE).pack()

        self.__linkEntry = Entry(self, **ENTRY_STYLE, textvariable=self.__linkValue)
        self.__linkEntry.pack(fill=X, padx=10, pady=5)

        self.__downloadBtn = Button(self, text="Download", **BTN_STYLE, command=lambda: self.__OnDownloadClick())
        self.__downloadBtn.pack(fill=X, padx=10, pady=5)

        self.__selectPath = Button(self, text="Select path", **BTN_STYLE, command=lambda: self.__choseDirectory())
        self.__selectPath.pack(fill=X, padx=10, pady=5)

        self.__saveFolder = BooleanVar()
        self.__saveFolderCheckBox = Checkbutton(self, text="Save to folder", **CHK_STYLE, variable=self.__saveFolder)
        self.__saveFolderCheckBox.select()
        self.__saveFolderCheckBox.pack(anchor="w", padx=10, pady=2)

        self.__saveArchive = BooleanVar()
        self.__saveArchiveCheckBox = Checkbutton(self, text="Save to archive", **CHK_STYLE, variable=self.__saveArchive)
        self.__saveArchiveCheckBox.pack(anchor="w", padx=10, pady=2)

        self.__savePicture = BooleanVar()
        self.__savePictureCheckBox = Checkbutton(self, text="Save with pictures", **CHK_STYLE, variable=self.__savePicture)
        self.__savePictureCheckBox.select()
        self.__savePictureCheckBox.pack(anchor="w", padx=10, pady=2)

        self.__savePSD = BooleanVar()
        self.__savePSDCheckBox = Checkbutton(self, text="Save with PSD", **CHK_STYLE, variable=self.__savePSD)
        self.__savePSDCheckBox.pack(anchor="w", padx=10, pady=2)

        self.__MangaAsyncDownloader = MangaAsyncDownloader()

        self.__async_loop = asyncio.new_event_loop()

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

        self.__progressBar = Progressbar(self, length=100, style="Custom.Horizontal.TProgressbar")
        self.__progressBar.pack(fill=X, padx=10, pady=5)


    def __StartDownload(self, path: str, link: str, download_mode: DownloadMode, on_end, on_update):
        asyncio.set_event_loop(self.__async_loop)
        self.__async_loop.run_until_complete(
            self.__MangaAsyncDownloader.SaveAllChapters(
                link=link,
                path=path,
                start_counter=1,
                download_mode=download_mode,
                on_update=on_update
            )
        )
        on_end()

    def __OnLinkChange(self):
        posterLink = MangaDownloader.GetPoster(self.__linkValue.get())
        if not posterLink is None:
            self.master.LoadPoster(posterLink)

    def __OnDownloadClick(self):

        if self.__MangaAsyncDownloader.IsWorking:
            self.__MangaAsyncDownloader.Stop()
            return

        print("Downloading...")
        link = self.__linkValue.get()

        try:
            requests.get(link)
        except:
            print("Aborting...")
            messagebox.showerror("Error", f"Could not download from {link}")
            return

        if (not self.__saveFolder.get()) and (not self.__saveArchive.get()):
            print("Aborting...")
            messagebox.showerror("Error", "Please select a folder or archive saving mode")
            return

        if (not self.__savePicture.get()) and (not self.__savePSD.get()):
            print("Aborting...")
            messagebox.showerror("Error", "Please select a pictures or PSD saving mode")
            return

        download_mod = DownloadMode.NULL

        if self.__savePicture.get():
            download_mod |= DownloadMode.SAVE_PICTURES

        if self.__savePSD.get():
            download_mod |= DownloadMode.SAVE_PSD

        if self.__saveFolder.get():
            download_mod |= DownloadMode.SAVE_TO_FOLDER

        if self.__saveArchive.get():
            download_mod |= DownloadMode.SAVE_TO_ARCHIVE

        download_mod |= DownloadMode.MARK_NUMERATION

        self.__downloadBtn['text'] = "Stop"

        def on_end():
            self.__downloadBtn['text'] = "Download"
            messagebox.showinfo("Download Complete", "Download Complete")
            self.__progressBar.config(value=0)

        chapters_number = MangaDownloader.GetChaptersNumber(link)

        def on_update():
            self.__progressBar.step(100 / chapters_number)

        downloadThread = Thread(
            target=self.__StartDownload,
            args=(self.__savePath.get(), link, download_mod, on_end, on_update)
        )
        downloadThread.start()


    def __choseDirectory(self):
        folder_path = filedialog.askdirectory(title="Оберіть папку для збереження")
        if folder_path:
            self.__savePath.set(folder_path)


