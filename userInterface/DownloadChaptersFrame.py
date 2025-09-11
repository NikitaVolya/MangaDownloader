from tkinter import *

from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style, Treeview, Combobox

import requests

from downloaders import MangaRequestsDownloader, MangaDexDownloader
from downloaders.IMangaDownloader import IMangaDownloader
from parsers import BatoToParser, XBatoParser

from userInterface.Setup import ENTRY_STYLE, BTN_STYLE, LABEL_STYLE, CHK_STYLE, APP_BACKGROUND
from enums import DownloadMode

from threading import Thread


class DownloadChaptersFrame(Frame):

    def __init__(self, master: "MainWindow"):
        super().__init__(master, bg=APP_BACKGROUND)

        self.master: "MainWindow" = master


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
        style.configure(
            "Custom.Treeview",
            background=APP_BACKGROUND,
            foreground="white",
            fieldbackground=APP_BACKGROUND
        )
        style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", "#2d2d2d"), ("!disabled", "#2d2d2d")],
            foreground=[("readonly", "white"), ("!disabled", "white")],
        )

        style.configure(
            "Custom.TCombobox",
            fieldbackground="#2d2d2d",
            background="#2d2d2d",
            foreground="white",
            selectbackground="#007acc",
            selectforeground="white",
            arrowcolor="white",
            borderwidth=0,
            relief=FLAT,
            padding=5
        )



        Label(self, text="Site for manga", **LABEL_STYLE).pack()

        self.__selected_site = StringVar()
        self.__size_combo = Combobox(
            self,
            textvariable=self.__selected_site,
            values=["Bato.To", "MangoDex", "XBato.com"],
            style="Custom.TCombobox",
            state="readonly"
        )
        self.__size_combo.pack(fill=X, padx=10, pady=5)

        self.__size_combo.bind("<<ComboboxSelected>>", lambda e: self.ChangeSite(self.__selected_site.get()))

        Label(self, text="Link to main page of manga", **LABEL_STYLE).pack()

        self.__linkValue = StringVar()
        self.__linkValue.trace_add("write", lambda *args: self.__OnLinkChange())

        self.__savePath = StringVar()
        self.__savePath.set("download")


        self.__linkEntry = Entry(self, **ENTRY_STYLE, textvariable=self.__linkValue)
        self.__linkEntry.pack(fill=X, padx=10, pady=5)

        self.__selectPath = Button(self, text="Select path", **BTN_STYLE, command=lambda: self.__choseDirectory())
        self.__selectPath.pack(fill=X, padx=10, pady=5)

        self.__selectedChapters = None
        self.__chapters = []
        self.__tree = Treeview(self, columns=["Chapter"], show="headings", selectmode="extended", style="Custom.Treeview")
        self.__tree.heading("Chapter", text="Chapters")
        self.__tree.column("Chapter", width=300)
        self.__tree.pack(expand=True)

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

        self.__mergeFrames = BooleanVar()
        self.__mergeFramesCheckBox = Checkbutton(self, text="Merge frames", **CHK_STYLE, variable=self.__mergeFrames)
        self.__mergeFramesCheckBox.pack(anchor="w", padx=10, pady=2)

        self.__downloadBtn = Button(self, text="Download", **BTN_STYLE, command=lambda: self.__OnDownloadClick())
        self.__downloadBtn.pack(fill=X, padx=10, pady=5)

        self.__progressBar = Progressbar(self, length=100, style="Custom.Horizontal.TProgressbar")
        self.__progressBar.pack(fill=X, padx=10, pady=5)

        self.__mangaDownloader: IMangaDownloader = None

    def ChangeSite(self, name: str):
        print(f"Change site to {name}")
        self.__selected_site.set(name)
        if name == "Bato.To":
            self.__mangaDownloader = MangaRequestsDownloader(BatoToParser())
        elif name == "MangoDex":
            self.__mangaDownloader = MangaDexDownloader()
        elif name == "XBato.com":
            self.__mangaDownloader = MangaRequestsDownloader(XBatoParser())
        else:
            messagebox.showerror("Error", "Invalid site")
            self.__selected_site.set("")


    def UpdateSelectedChapters(self):
        selection = self.__tree.selection()
        result = [self.__chapters[int(iid)] for iid in selection]
        self.__selectedChapters = result if len(result) > 0 else None

    def __OnLinkChange(self):

        manga_link: str = self.__linkEntry.get()

        if manga_link.lower().startswith("https://bato.si"):
            site_name = "Bato.To"
        elif manga_link.lower().startswith("https://mangadex.org"):
            site_name = "MangoDex"
        elif manga_link.lower().startswith("https://xbato.com"):
            site_name = "XBato.com"
        else:
            messagebox.showerror("Error", "Invalid site")
            return

        if site_name != self.__selected_site.get():
            self.ChangeSite(site_name)

        poster_link = self.__mangaDownloader.GetPosterLink(manga_link)
        if poster_link is None:
            return

        self.master.LoadPoster(poster_link)

        self.__chapters = self.__mangaDownloader.GetChapters(manga_link)
        for i, chapter in enumerate(self.__chapters):
            print(chapter)
            self.__tree.insert('', END, iid=str(i), values=(chapter.Title,))

    def __StartDownload(self):
        self.__mangaDownloader.DownloadChapters(
                link=self.__linkValue.get(),
                path=self.__savePath.get(),
                chapters=self.__selectedChapters
            )

        self.__downloadBtn['text'] = "Download"
        messagebox.showinfo("Download Complete", "Download Complete")
        self.__progressBar.config(value=0)

    def __OnDownloadClick(self):

        if self.__mangaDownloader.IsWorking:
            self.__mangaDownloader.Stop()
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

        if (not self.__savePicture.get()) and (not self.__savePSD.get() and (not self.__mergeFrames.get())):
            print("Aborting...")
            messagebox.showerror("Error", "Please select a pictures or PSD saving mode")
            return

        self.UpdateSelectedChapters()

        if self.__selectedChapters is None:
            print("Aborting...")
            messagebox.showerror("Error", "Chapters are not selected")
            return

        download_mode = DownloadMode.NULL

        if self.__savePicture.get():
            download_mode |= DownloadMode.SAVE_PICTURES

        if self.__savePSD.get():
            download_mode |= DownloadMode.SAVE_PSD

        if self.__saveFolder.get():
            download_mode |= DownloadMode.SAVE_TO_FOLDER

        if self.__saveArchive.get():
            download_mode |= DownloadMode.SAVE_TO_ARCHIVE

        if self.__mergeFrames.get():
            download_mode |= DownloadMode.MERGE_PICTURES

        self.__mangaDownloader.DownloadMode = download_mode

        self.__downloadBtn['text'] = "Stop"

        def on_update():
            self.__progressBar.step(100 / len(self.__selectedChapters))
        self.__mangaDownloader.OnDownloadChapterFinished = on_update

        downloadThread = Thread(target=self.__StartDownload)
        downloadThread.start()


    def __choseDirectory(self):
        folder_path = filedialog.askdirectory(title="Оберіть папку для збереження")
        if folder_path:
            self.__savePath.set(folder_path)


