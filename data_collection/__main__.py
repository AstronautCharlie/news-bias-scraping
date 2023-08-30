import logging
from time import sleep
from scraping.app import App
from settings import AppConfig
import os 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Wait to let Selenium spin up before running
    startup_timer = AppConfig.STARTUP_TIMER
    if startup_timer > 0:
        logger.info(f'Sleeping for {startup_timer} before startup to let Selenium spin up')
        sleep(startup_timer)
    app = App()
    
    app.run()
    logger.info(f'Scrape completed. Goodbye :)')