import logging
from time import sleep
from scraping.app import App
from settings import AppConfig

logging.basicConfig(level=AppConfig.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sleep(5) # For startup - otherwise this crashes
    app = App()
    app.run()    