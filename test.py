import requests
from bs4 import BeautifulSoup as BS


URL = 'https://store.epicgames.com/ru/free-games'

r = requests.get(URL)
html = BS(r.content, 'lxml')

freeGamesHtml = html.findAll('div', class_='css-11xvn05')
print(freeGamesHtml)
# freeGames = html.find('div', class_='css-1myhtyb')

