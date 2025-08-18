import os

from downloaders.strategies.DownloadStrategy import DownloadStrategy
from outils import Convertor


class SavePSDStrategy(DownloadStrategy):


    def Execute(self, path: str):
        files = os.listdir(path)
        for file in filter(lambda f: f.lower().endswith(".jpg"), files):
            Convertor.SaveAsPSD(f"{path}/{file}", f"{path}/{file.replace(".jpg", ".psd")}")
