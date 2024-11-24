import time
from abc import ABC, abstractmethod
from tempfile import mkdtemp

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from llm_engineering.domain.documents import NoSQLBaseDocument

chromedriver_autoinstaller.install()


class BaseCrawler(ABC):

    model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None:

        pass


class BaseSeleniumCrawler(BaseCrawler, ABC):

    __slots__ = "_options", "_scroll_limit", "_driver"

    def __init__(self, scroll_limit: int = 5) -> None:

        _options = webdriver.ChromeOptions()

        _options.add_argument("--no-sandbox")
        _options.add_argument("--headless=new")
        _options.add_argument("--disable-dev-shm-usage")
        _options.add_argument("--log-level=3")
        _options.add_argument("--disable-popup-blocking")
        _options.add_argument("--disable-notifications")
        _options.add_argument("--disable-extensions")
        _options.add_argument("--disable-background-networking")
        _options.add_argument("--ignore-certificate-errors")
        _options.add_argument(f"--user-data-dir={mkdtemp()}")
        _options.add_argument(f"--data-path={mkdtemp()}")
        _options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        _options.add_argument("--remote-debugging-port=9226")

        self.set_extra_driver_options(_options)
        self._scroll_limit = scroll_limit
        self._driver = webdriver.Chrome(options=_options)

    def set_extra_driver_options(self, options: Options) -> None:
        pass

    def login(self) -> None:
        pass

    def scroll_page(self) -> None:
        """Scroll through page on the scroll limit"""
        current_scroll = 0
        last_height = self._driver.execute_script("return document.body.scrollHeight")
        while True:
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self._driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or(self._scroll_limit and current_scroll >= self._scroll_limit):
                break
            last_height = new_height
            current_scroll += 1


