
from userInterface.DownloadChaptersFrame import DownloadChaptersFrame
from userInterface.WebPoster import WebPoster


from tkinter import Tk, PhotoImage


class MainWindow(Tk):

    def __init__(self):
        super().__init__()

        self.title("Manga Downloader")
        self.geometry("750x700")
        self.configure(bg="#1e1e1e")

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.poster = WebPoster(self, (350, 500))

        self.__currentFrame = DownloadChaptersFrame(self)
        self.__currentFrame.grid(row=0, column=0, sticky="nsew")

        self.__icon = PhotoImage(file="src/icon.png")
        self.iconphoto(False, self.__icon)

