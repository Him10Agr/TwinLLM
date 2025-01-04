from urllib.parse import urlparse
from loguru import logger
from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

from llm_engineering.application.crawlers.dispatcher import CrawlersDispatcher
from llm_engineering.domain.documents import UserDocument


@step
def crawl_links(user: UserDocument, links: list[str]) -> Annotated[list[str], "crawled_links"]:

    dispatcher = CrawlersDispatcher.build().register_linkedin().register_github().register_medium()
    logger.info(f"Starting to crawl {len(links)} link(s).")

    metadata = {}
    successful_crawls = 0
    for link in tqdm(links):
        successful_crawl, crawled_domain = _crawl_link(dispacther=dispatcher, link=link, user=user)
        successful_crawls += successful_crawl

        metadata = _add_to_metadata(metadata=metadata, domain=crawled_domain, successfull_crawl=successful_crawl)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="crawled_links", metadata=metadata)

    logger.info(f"Successfully crawled {successful_crawls} / {len(links)} links.")

    return links
    

def _crawl_link(dispacther: CrawlersDispatcher, link: str, user: UserDocument) -> tuple[bool, str]:

    crawler = dispacther.get_crawler(link)
    crawler_domain = urlparse(link).netloc

    try:

        crawler.extract(link = link, user = user)
        return (True, crawler_domain)
    except Exception as e:

        logger.error(f"An error occured while crawling: {e!s}")
        return (False, crawler_domain)


def _add_to_metadata(metadata: dict, domain: str, successfull_crawl: bool) -> dict:
    if domain not in metadata:
        metadata[domain] = {}
    metadata[domain]["successfull"] = metadata.get(domain, {}).get("successful", 0) + successfull_crawl
    metadata[domain]["total"] = metadata.get(domain, {}).get("total", 0) + 1

    return metadata

