import asyncio
from multiprocessing import Process

# Crawlee imports
from crawlee import  Request
from crawlee.playwright_crawler import PlaywrightCrawler
from crawlee.http_clients._httpx import HttpxHttpClient
from crawlee import ConcurrencySettings
from crawlee.proxy_configuration import ProxyConfiguration
from crawlee.storages import Dataset

# Local imports
from utils.AIUtil import getMatchingRegexPattern
from app.routers.IntialMetadataRouter import router as IntialRouteToFindPatternRouter
from app.triggers.fullWebsite import runMainlCrawl

import traceback


from utils.log import loggerClass

lg = loggerClass('generalised-crawler.log')
async def triggerInitialCrawl(url) -> None:
    try:
        """The Initial crawler entry point."""
        # dataset = await Dataset.open(id="initial",name="initial")
        # Configuration.set('local_directory', './my-custom-directory')
        
        crawler = PlaywrightCrawler(
            headless=True,
            request_handler=IntialRouteToFindPatternRouter,
            max_requests_per_crawl=5,
            
        )

        # await crawler.run(
        #     [
        #         'https://www.flipkart.in/',
        #     ]
        # )
        request = Request.from_url(url)

        lg.logger.info("Intil crawl triggered 2 ...")
        await crawler.run(
            [request]
        )
        export_data_json = await crawler.get_data()
        
        lg.logger.info(export_data_json)
        allCrawledObjs = export_data_json.items
        
        all_urls = []
        for obj in allCrawledObjs:
            all_urls.append(obj['url'])
        
        lg.logger.info(f"URLs used for detecting pattern {len(all_urls)}")
        pattern = getMatchingRegexPattern(all_urls)
        lg.logger.info(f"Detected patter: {pattern}")
        
        if(pattern == None):
            lg.logger.info("Issue in detecting pattern")
            return
        
        lg.logger.info("Starting main crawl...")
        mainProcess = Process(target=runMainlCrawl, args=(url,pattern,))
        mainProcess.start()
    except Exception as e:
        lg.logger.error("issue in initiating initial crawl")
        lg.logger.error(e)
        lg.logger.error(traceback.format_exc())
    

def runIntialCrawl(url):
    """Function to run the async trigger_crawl in a separate thread."""
    lg.logger.info("Intial crawl triggered 1 ...")
    asyncio.run(triggerInitialCrawl(url))