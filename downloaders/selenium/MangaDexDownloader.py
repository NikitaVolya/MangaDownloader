from selenium.webdriver.support.expected_conditions import visibility_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait

from downloaders.IMangaDownloader import IMangaDownloader
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from entity import MangaChapter

import time


class MangaDexDownloader(IMangaDownloader):

    __options = Options()
    __options.add_argument('--headless')

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

        rep: list[MangaChapter] = []

        while True:
            page_buttons = self.__driver.find_elements(By.XPATH, "//div[@class='flex justify-center flex-wrap gap-2 mt-6']/button")

            next_button = page_buttons[-1] if len(page_buttons) > 0 else None

            chapters = WebDriverWait(self.__driver, 10).until(
                visibility_of_all_elements_located((By.XPATH, "//div[@class='bg-accent rounded-sm']"))
            )

            for chapter in chapters:
                lines = chapter.find_elements(By.XPATH, "div")

                title = chapter.find_element(By.CLASS_NAME, "chapter-link" if len(lines) == 1 else "chapter-header").text
                href = chapter.find_elements(By.CLASS_NAME, "chapter-grid")[0].get_attribute("href")

                rep.append(MangaChapter(href, title))

            if next_button is None or "disabled" in next_button.get_attribute("class"):
                break

            next_button.click()
        return rep

    def DownloadMangaPages(self, link: str, path = "download") -> list[str]:
        self.__driver.get(link)

        menuButton = WebDriverWait(self.__driver, 10).until(
            visibility_of_all_elements_located(
                (By.CLASS_NAME, "menu")
            )
        )
        time.sleep(1)
        try:
            menuButton[0].click()
        except:
            pass

        time.sleep(1)
        menuOptions = WebDriverWait(self.__driver, 10).until(
            visibility_of_all_elements_located(
                (By.XPATH, '//div[@class="flex flex-col gap-2"]/button')
            )
        )

        while True:
            if menuOptions[0].text.lower() == "long strip":
                break
            menuOptions[0].click()

        rep: list[str] = []

        nextChapterButton = None
        try:
            nextChapterButton = WebDriverWait(self.__driver, 3).until(
                visibility_of_all_elements_located(
                    (By.XPATH, "//span[text()='Next Chapter']")
                )
            )
        except:
            pass

        if nextChapterButton is None:
            nextChapterButton = WebDriverWait(self.__driver, 3).until(
                visibility_of_all_elements_located(
                    (By.XPATH, "//span[text()='Return to title page']")
                )
            )

        time.sleep(2)

        self.__driver.execute_script("arguments[0].scrollIntoView()", nextChapterButton[0])

        pages = WebDriverWait(self.__driver, 10).until(
            visibility_of_all_elements_located(
                (By.XPATH, "//div[@class='md--page ls limit-width limit-height mx-auto']/img")
            )
        )

        for i, page in enumerate(pages):
            image_path = f"{path}/{i + 1}.jpg"
            with open(image_path, "wb") as f:
                f.write(page.screenshot_as_png)
            rep.append(image_path)
        return rep
