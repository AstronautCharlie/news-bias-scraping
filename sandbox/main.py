from time import sleep
import logging 
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

from app import App

app = App() 

logger.info('Running app')
app.run()
sleep(600)