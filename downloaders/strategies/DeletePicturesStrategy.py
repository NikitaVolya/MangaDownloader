import os

from downloaders.strategies.DownloadStrategy import DownloadStrategy


class DeletePicturesStrategy(DownloadStrategy):

    def Execute(self, path: str):
        files = os.listdir(path)
        for file in filter(lambda f: f.endswith(".jpg"), files):
            os.remove(f"{path}/{file}")