from downloaders.strategies import DownloadStrategy
import os


class DeleteFolderStrategy(DownloadStrategy):

    def Execute(self, path: str):

        for files in os.listdir(path):
            os.remove(f"{path}/{files}")
        os.removedirs(path)