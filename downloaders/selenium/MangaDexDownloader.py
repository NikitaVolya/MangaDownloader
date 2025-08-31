from selenium.webdriver.support.expected_conditions import visibility_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait

from downloaders.selenium.MangaDownloader import MangaDownloader
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import base64
import requests

from entity import MangaChapter


class MangaDexDownloader(MangaDownloader):

    __options = Options()
    __options.add_argument('--headless')
    __options.set_preference("media.volume_scale", "0.0")

    def __init__(self):

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

    def GetMangaPages(self, link: str) -> list[str]:
        self.__driver.get(link)

        try:
            rep: list[str] = []

            pages = WebDriverWait(self.__driver, 2000).until(
                visibility_of_all_elements_located(
                    (By.XPATH, "//div[@class='md--page ls limit-width mx-auto']/img")
                )
            )

            for i, page in enumerate(pages):
                image_href = page.get_attribute("src")
                rep.append(image_href)

                with open(f"download/{i + 1}.png", "wb") as f:
                    f.write(page.screenshot_as_png)
            return rep
        except Exception as e:
            print(e)
            return []

    def DownloadPage(self, link: str):
        self.__driver.get(link)
        img = self.__driver.find_element(By.TAG_NAME, "img")