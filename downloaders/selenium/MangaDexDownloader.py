from selenium.webdriver.support.expected_conditions import visibility_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait

from downloaders.IMangaDownloader import IMangaDownloader
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from entity import MangaChapter
from outils import Convertor

from time import sleep

import os


class MangaDexDownloader(IMangaDownloader):

    __options = Options()
    __options.add_argument('--headless')
    __options.set_preference("media.volume_scale", "0.0")

    def __init__(self):
        super().__init__()

        self.__driver = Firefox(options=MangaDexDownloader.__options)

    def __del__(self):
        self.__driver.quit()

    def GetPosterLink(self, link: str) -> str | None:

        self.__driver.get(link)
        try:
            image = WebDriverWait(self.__driver, 10).until(
                visibility_of_all_elements_located((By.XPATH, "//img[@alt='Cover image']"))
            )
            return image[0].get_attribute("src")
        except:
            return None

    def GetTitle(self, link: str) -> str | None:
        self.__driver.get(link)

        try:
            title = WebDriverWait(self.__driver, 10).until(
                visibility_of_all_elements_located((By.XPATH, "//div[@class='title']/p"))
            )
            return title[0].text
        except:
            return None

    def GetChapters(self, link: str) -> list[MangaChapter]:
        self.__driver.get(link)

        try:
            rep: list[MangaChapter] = []

            while True:
                page_buttons = WebDriverWait(self.__driver, 10).until(
                    visibility_of_all_elements_located(
                        (By.XPATH, "//div[@class='flex justify-center flex-wrap gap-2 mt-6']/button")
                    )
                )

                next_button = page_buttons[-1]

                chapters = WebDriverWait(self.__driver, 10).until(
                    visibility_of_all_elements_located((By.XPATH, "//div[@class='bg-accent rounded-sm']"))
                )

                for chapter in chapters:
                    lines = chapter.find_elements(By.XPATH, "div")

                    title = chapter.find_element(By.CLASS_NAME, "chapter-link" if len(lines) == 1 else "chapter-header").text
                    href = chapter.find_elements(By.CLASS_NAME, "chapter-grid")[0].get_attribute("href")

                    rep.append(MangaChapter(href, title))

                if "disabled" in next_button.get_attribute("class"):
                    break

                next_button.click()
            return rep
        except Exception as e:
            print(e)
            return []

    def DownloadMangaPages(self, link: str, path = "download") -> list[str]:
        self.__driver.get(link)

        try:
            rep: list[str] = []

            nextChapterButton = WebDriverWait(self.__driver, 10).until(
                visibility_of_all_elements_located(
                    (By.XPATH, "//span[text()='Next Chapter']")
                )
            )[0]

            self.__driver.execute_script("arguments[0].scrollIntoView()", nextChapterButton)

            sleep(2)

            pages = WebDriverWait(self.__driver, 5000).until(
                visibility_of_all_elements_located(
                    (By.XPATH, "//div[@class='md--page ls limit-width mx-auto']/img")
                )
            )

            for i, page in enumerate(pages):
                image_path = f"{path}/{i + 1}.jpg"
                with open(image_path, "wb") as f:
                    f.write(page.screenshot_as_png)
                rep.append(image_path)
            return rep
        except Exception as e:
            print(e)
            return []

    def DownloadChapter(self, manga_chapter: MangaChapter, path = "download"):

        chapter_path = f"{path}/{Convertor.ToSave(manga_chapter.Title)}"
        os.makedirs(chapter_path, exist_ok=True)
        self.DownloadMangaPages(manga_chapter.Href, chapter_path)

        for strategy in self._strategies:
            strategy.Execute(chapter_path)

    def DownloadChapters(self, link: str, path: str = "download", chapters: list[MangaChapter] = None) -> None:

        title = Convertor.ToSave(self.GetTitle(link))
        os.makedirs(f"{path}/{title}", exist_ok=True)

        if chapters is None:
            chapters: list[MangaChapter] = self.GetChapters(link)

        for chapter in chapters:
            while True:
                print("Starting chapter:", chapter.Href)
                try:
                    self.DownloadChapter(chapter, f"{path}/{title}")
                except Exception as e:
                    print("Error chapter", chapter.Href, "Error:", e)
                    print("Retrying...", chapter.Href)
                    continue
                break
            if self.OnDownloadChapterFinished:
                self.OnDownloadChapterFinished()