from selenium.webdriver.support.expected_conditions import visibility_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait

from downloaders.IMangaDownloader import IMangaDownloader
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from entity import MangaChapter

import time


class HoneyMangaDownloader(IMangaDownloader):

    __options = Options()
    __options.add_argument('--headless')

    def __init__(self):
        super().__init__()

        self.__driver = Firefox(options=HoneyMangaDownloader.__options)

    def __del__(self):
        self.__driver.quit()

    def GetPosterLink(self, link: str) -> str | None:
        self.__driver.get(link)

        elements = WebDriverWait(self.__driver, 10).until(
            visibility_of_all_elements_located(
                (By.XPATH, "//img[@class='object-center object-cover h-full w-full rounded-[4px]']")
            )
        )
        if len(elements) == 0:
            return None
        return elements[0].get_attribute("src")

    def GetTitle(self, link: str) -> str | None:
        self.__driver.get(link)

        elements = WebDriverWait(self.__driver, 10).until(
            visibility_of_all_elements_located(
                (By.XPATH, "//div/p[@class='max-md:text-center font-bold text-lg dark:text-white text-gray-700']")
            )
        )
        if len(elements) == 0:
            return None
        return elements[0].text

    def GetChapters(self, link: str) -> list[MangaChapter]:
        self.__driver.get(link)
        self.__driver.execute_script("localStorage.setItem('ADULT_MODE', true)")
        self.__driver.get(link)

        endFlag = False

        rep = []

        while True:
            time.sleep(1)
            elements = self.__driver.find_elements(By.XPATH, "//li/button[@class='MuiButtonBase-root MuiPaginationItem-root MuiPaginationItem-sizeMedium MuiPaginationItem-text MuiPaginationItem-rounded MuiPaginationItem-previousNext css-i4f9pm']")

            time.sleep(1)

            chapters = WebDriverWait(self.__driver, 10).until(
                visibility_of_all_elements_located(
                    (By.XPATH, "//a[@class='flex items-start justify-between py-4 border-b last:border-b-0 border-dashed dark:border-gray-800 border-gray-200']")
                )
            )

            for chapter in chapters:
                chapterHref = chapter.get_attribute("href")
                chapterTitle = chapter.find_element(By.CLASS_NAME, "font-medium").text

                rep.append(
                    MangaChapter(chapterHref, chapterTitle)
                )


            if len(elements) == 0 or (len(elements) == 1 and endFlag):
                break
            elif len(elements) == 1:
                elements[0].click()
            else:
                elements[1].click()

            endFlag = True

        return rep

    def DownloadMangaPages(self, link: str, path = "download") -> list[str]:
        self.__driver.get(link)
        self.__driver.execute_script('document.getElementsByClassName("grid-cols-12")[0].style.visibility = "hidden";')

        lastNumber = 0
        pages = []

        time.sleep(4)

        while True:
            pages = self.__driver.find_elements(
                By.XPATH, "//div[@class='relative dark:bg-gray-800 bg-gray-200 MuiBox-root css-1pffsdl']/span[@class=' lazy-load-image-background opacity lazy-load-image-loaded']/img"
            )

            self.__driver.execute_script("arguments[0].scrollIntoView();", pages[-1])
            self.__driver.execute_script("window.scrollBy(0,arguments[0])", pages[-1].size["height"] + 500)
            time.sleep(4)

            if lastNumber == len(pages):
                break
            lastNumber = len(pages)


        rep: list[str] = []

        for i, page in enumerate(pages):
            image_path = f"{path}/{i + 1}.jpg"
            with open(image_path, "wb") as f:
                f.write(page.screenshot_as_png)
            rep.append(image_path)
        return rep