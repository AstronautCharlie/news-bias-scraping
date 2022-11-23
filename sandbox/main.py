from time import sleep
import logging 
logging.basicConfig(level=logging.INFO)
       
from app import App

app = App() 

app.run()
