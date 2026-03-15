import requests
from bs4 import BeautifulSoup
import time
import xml

url = requests.get('https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml?iss.dp=comma&iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST')
