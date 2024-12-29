import asyncio
import os
import uuid

# Crawlee imports
from crawlee import Request
from crawlee.playwright_crawler import PlaywrightCrawler
from crawlee.http_clients._httpx import HttpxHttpClient
from crawlee import ConcurrencySettings
from crawlee.proxy_configuration import ProxyConfiguration

# Local imports
from utils.AIUtil import getMatchingRegexPattern
from app.routers.mainRouter import router as mainRouter

import traceback


from utils.log import loggerClass

lg = loggerClass('generalised-crawler.log')

def runMainlCrawl(url,regexPattern):
    """Function to run the async trigger_crawl in a separate thread."""
    lg.logger.info("Main crawl triggered 1 ...")
    asyncio.run(triggerMainCrawl(url,regexPattern))
    lg.logger.info("Main crawl ended.")
    
    
async def triggerMainCrawl(url,regexPattern):
    try:
        
        #Concurrency Settings, set according to available compute and un comment in crawler intialise
        
        concurrency_settings = ConcurrencySettings(
        # Start with 8 concurrent tasks, as long as resources are available.
        desired_concurrency=8,
        # Maintain a minimum of 5 concurrent tasks to ensure steady crawling.
        min_concurrency=5,
        # Limit the maximum number of concurrent tasks to 10 to prevent
        # overloading the system.
        max_concurrency=10,
    )
        #Proxy settings to help if website has IP blocking
        proxy_configuration = ProxyConfiguration(
            proxy_urls=[
                'http://proxy-1.com/',
                'http://proxy-2.com/',
            ]
        )
        unique_dir = f"./custom-data-directory-{uuid.uuid4()}"
        os.environ['CRAWLEE_STORAGE_DIR'] = unique_dir

        crawler = PlaywrightCrawler(
            headless=True,
            request_handler=mainRouter,
            
            #Uncomment for testing
            max_requests_per_crawl=20,
            
            # Uncomment in production
            # concurrency_settings=concurrency_settings,
            # proxy_configuration=proxy_configuration,
        )

        lg.logger.info("Main crawl triggered 2 ...")
        request = Request.from_url(url,user_data={'regex': regexPattern })


        await crawler.run(
            [request]
        )
    except Exception as e:
        lg.logger.error("issue in initiating initial crawl")
        lg.logger.error(e)
        lg.logger.error(traceback.format_exc())
    