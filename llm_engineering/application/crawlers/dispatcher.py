import re
from urllib.parse import urlparse

from loguru import logger

from .base import BaseCrawler
from .custom_article import CustomArticleCrawler
from .github import GithubCrawler
from .linkedin import LinkedInCrawler
from .medium import MediumCrawler


class CrawlersDispatcher:

    __slots__ = "_crawlers"

    def __init__(self) -> None:
        
        self._crawlers = {}

    @classmethod
    def build(cls) -> "CrawlersDispatcher":

        dispatcher = cls()

        return dispatcher
    
    def _register(self, domain: str, crawler: type[BaseCrawler]) -> None:

        parsed_url = urlparse(domain)
        domain = parsed_url.netloc

        self._crawlers[r"https://(www\.)?{}/*".format(re.escape(domain))] = crawler

    def register_medium(self) -> "CrawlersDispatcher":

        self._register("https://medium.com", MediumCrawler)

        return self
    
    def register_linkedin(self) -> "CrawlersDispatcher":

        self._register("https://www.linkedin.com", LinkedInCrawler)

        return self
    
    def register_github(self) -> "CrawlersDispatcher":

        self._register("https://www.github.com", GithubCrawler)

        return self
    
    def get_crawler(self, url: str) -> BaseCrawler:

        for pattern, crawler in self._crawlers.items():

            if re.match(pattern, url):
                return crawler()
            
        logger.warning(f"No crawler found for {url}. Defaulting to CustomArticleCrawler.")

        return CustomArticleCrawler()



    
