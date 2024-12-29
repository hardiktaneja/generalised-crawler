from urllib.parse import urljoin
import re
import asyncio
from contextlib import suppress, asynccontextmanager

# Crawlee imports
from crawlee import Request
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from crawlee.router import Router

# Import traceback at the end to avoid circular import issues
import traceback

# Import playwright.async_api after Crawlee imports to avoid potential conflicts
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


# from crawlee.storages.dataset import Dataset

router = Router[PlaywrightCrawlingContext]()

def is_product_url(url: str, regex) -> bool:
    """
    This function checks if a URL from Amazon is likely a product URL.

    Args:
        url: The URL to be checked.

    Returns:
        True if the URL likely points to a product, False otherwise.
    """
    if(re.search(regex,url)):
        return True

    return False

async def accept_cookies(page: Page):
    task = asyncio.create_task(page.get_by_test_id('dialog-accept-button').click())
    try:
        yield
    finally:
        if not task.done():
            task.cancel()

        with suppress(asyncio.CancelledError, PlaywrightTimeoutError):
            await task


@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    """Default request handler for main web crawl."""
    try:
        # Infinite scroll to the page if available
        # await context.page.wait_for_load_state('networkidle')
        # await context.infinite_scroll()            
        

        print(f'Processing {context.request.url} ...')
        

        # Locate all links by a broader selector if needed
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
                    is_pdt = is_product_url(full_url,context.request.user_data['regex'])
                    print(f"Link found: {full_url}, is_pdt: {is_pdt}, regex: {context.request.user_data['regex']}")
                    if(is_pdt):
                        await context.push_data(
                            {
                                'url': full_url,
                            }
                        )
                    else:
                        await context.add_requests([Request.from_url(full_url,user_data={'regex': context.request.user_data['regex']})])
            except Exception as e:
                print(e)
                
    except Exception as e:
        print(e)
        print(traceback.format_exc())