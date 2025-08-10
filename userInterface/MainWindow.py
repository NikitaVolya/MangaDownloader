
from PIL import Image, ImageTk
from io import BytesIO

from userInterface import DownloadChaptersFrame

from tkinter import Tk, Label, Frame, PhotoImage

import requests


class MainWindow(Tk):

    def __init__(self):
        super().__init__()

        self.title("Manga Downloader")
        self.geometry("750x340")
        self.configure(bg="#1e1e1e")

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.posterFrame = Frame(self, bg="#1e1e1e")
        self.posterFrame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.posterImg = ImageTk.PhotoImage(
            Image
               .new("RGB", (200, 280), color=(50, 50, 50))
               .resize((200, 280), Image.LANCZOS)
        )

        self.posterLabel = Label(self.posterFrame, image=self.posterImg, bg="#1e1e1e")
        self.posterLabel.pack(expand=True)

        self.__currentFrame = DownloadChaptersFrame(self)
        self.__currentFrame.grid(row=0, column=0, sticky="nsew")

        self.__icon = PhotoImage(file="src/icon.png")
        self.iconphoto(False, self.__icon)



    def LoadPoster(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((200, 280), Image.LANCZOS)
            self.posterImg = ImageTk.PhotoImage(img)
        except Exception as e:
            print("Error loading image:", e)
            img = Image.new("RGB", (200, 280), color=(50, 50, 50))
            self.posterImg = ImageTk.PhotoImage(img)

        self.posterLabel.config(image=self.posterImg)
        self.posterLabel.image = self.posterImg