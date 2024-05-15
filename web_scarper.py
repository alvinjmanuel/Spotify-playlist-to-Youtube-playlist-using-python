from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("https://www.youtube.com/results?search_query=meet+the+grahams+kendrick+lamar")

soup = BeautifulSoup(driver.page_source, 'html.parser')
links = soup.find_all("a", attrs={'id':'video-title'})
link = links[0].get('href')
print(link)

# url = "https://www.youtube.com/results?search_query=meet+the+grahams+kendrick+lamar"
# us = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
# HEADERS = ({'User-Agent':us, 'Accept-Language':'en-US, en;q=0.5'})

# webpage = requests.get(url,headers=HEADERS)

# soup = BeautifulSoup(webpage.content, "html.parser")
# links = soup.find(id="thumnbnail")
# print(links)