from urllib.parse import urljoin
import re
import asyncio
from contextlib import suppress, asynccontextmanager

# Crawlee imports
from crawlee import Request
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from crawlee.router import Router

import traceback

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError 


router = Router[PlaywrightCrawlingContext]()

@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    try:
        # async with accept_cookies(context.page):
        print(f'Processing {context.request.url} ...')
        all_links_locator = context.page.locator('a')  # General selector for anchor tags
        print(all_links_locator)
        # Get all elements matching the locator
        all_links = await all_links_locator.element_handles()

        # Debug: Print count of found links
        print(f"Found {len(all_links)} links on the page.")
  
        # Iterate through each link to get the href
        base_url = context.request.loaded_url
        for link in all_links:
            try:
                href = await link.get_attribute('href')
                if href:
                    
                    # Add this link to the request queue or handle it
                    full_url = urljoin(base_url, href)
                    
                    
                    await context.push_data(
                        {
                            'url': full_url,
                        }
                    )
                    
            except Exception as e:
                print(e)
        # await context.push_data(
        #     {
        #         'url': context.request.loaded_url,
        #     }
        # )
        await context.enqueue_links()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    
    
    