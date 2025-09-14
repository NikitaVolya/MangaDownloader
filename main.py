from registry import MangaDownloadersContainer
from userInterface import MainWindow


def Main():


    for downloaderData in MangaDownloadersContainer.DownloaderDataList():
        print(downloaderData.Name)

    window = MainWindow()
    window.mainloop()




if __name__ == "__main__":
    Main()