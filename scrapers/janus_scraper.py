import asyncio
import os
from dotenv import load_dotenv

from typing import Optional

from selenium_driverless import webdriver
# from selenium_driverless.types.by import By

# from utils.chromium_setup import setup_chromium

url = "https://uspdigital.usp.br/janus/componente/disciplinasOferecidasInicial.jsf"

async def janus_scraper(headless: bool = False, chromedriver_path: Optional[str] = None):

    load_dotenv(override=True)
    chromepath = os.getenv("CHROME_EXECUTABLE")
    if not chromepath and not chromedriver_path:
        raise KeyError("Could not find the path to a Chromium executable.")
    
    options = webdriver.ChromeOptions()
    options.binary_location = chromepath

    async with webdriver.Chrome(options=options) as driver:
        await driver.get(url, wait_load=True)
        print(driver.title)

if __name__ == "__main__":

    # setup_chromium()
    asyncio.run(janus_scraper())