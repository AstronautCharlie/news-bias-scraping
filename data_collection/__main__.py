import logging
from time import sleep
from scraping.app import App
from settings import AppConfig

logging.basicConfig(level=AppConfig.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Wait to let Selenium spin up before running
    startup_timer = AppConfig.STARTUP_TIMER
    if startup_timer > 0:
        logger.info(f'Sleeping for {startup_timer} before startup to let Selenium spin up')
        sleep(startup_timer)
    app = App()
    
    while True:
        app.run()
        logger.info(f'Scrape completed. Sleeping for {AppConfig.POLL_TIMER}')
        sleep(AppConfig.POLL_TIMER)