
from PIL import Image, ImageTk
from tkinter import Label, Frame

from io import BytesIO
import requests


class WebPoster:

    def __init__(self, master, size = tuple[int, int]):

        self.master = master

        self.__posterSize = size

        self.__posterFrame = Frame(master, bg="#1e1e1e")
        self.__posterFrame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.__posterImg = ImageTk.PhotoImage(
            Image
            .new("RGB", self.__posterSize, color=(50, 50, 50))
            .resize(self.__posterSize, Image.LANCZOS)
        )

        self.__posterLabel = Label(self.__posterFrame, image=self.__posterImg, bg="#1e1e1e")
        self.__posterLabel.pack(expand=True)

    @property
    def Size(self):
        return self.__posterSize

    def LoadPoster(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize(self.__posterSize, Image.LANCZOS)
            self.__posterImg = ImageTk.PhotoImage(img)
        except Exception as e:
            print("Error loading image:", e)
            img = Image.new("RGB", self.__posterSize, color=(50, 50, 50))
            self.__posterImg = ImageTk.PhotoImage(img)

        self.__posterLabel.config(image=self.__posterImg)
        self.__posterLabel.image = self.__posterImg
