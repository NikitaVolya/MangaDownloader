from downloaders.strategies.DownloadStrategy import DownloadStrategy
import os, patoolib

class ArchiveStrategy(DownloadStrategy):

    def Execute(self, path: str):

        cwd = os.getcwd()

        try:
            files = os.listdir(path)
            os.chdir(path)
            patoolib.create_archive(
                f"{cwd}\\{path}.zip",
                tuple(files),
            )
        finally:
            os.chdir(cwd)