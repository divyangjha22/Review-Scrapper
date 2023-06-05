import requests
from bs4 import BeautifulSoup

url = 'https://9animetv.to/home'
r = requests.get(url)

page = r.text

soup = BeautifulSoup(page, "lxml")

print(soup.div.p)
