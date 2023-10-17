import requests
from bs4 import BeautifulSoup as BS
import functions
import sqlite3

# functions.beggining()

r = requests.get('https://www.leagueoflegends.com/ru-ru/news/tags/patch-notes/')
html = BS(r.content, 'lxml')
url = 'https://www.leagueoflegends.com'
url += str(html.find('div', class_="style__WrapperInner-sc-106zuld-1 eInLGL").find('a').get('href'))
r = requests.get(url)
html = BS(r.content, 'lxml')
patch_html = html.find('section', class_='style__Wrapper-sc-133zq6e-0 kczDgl')

patch = patch_html.find('h1', class_='style__Title-vd48si-5 cmnoFj').text
print(patch + '\n')

updates_html = patch_html.findAll('div', class_='patch-change-block white-stone accent-before')
updates = []

con = sqlite3.connect('lol.db')
cur = con.cursor()
database_names = cur.execute('SELECT name FROM hero_names').fetchall()
con.close()

names_from_database = []
for el in database_names:
    names_from_database.append(el[0])

for el in updates_html:
    if '\n' in el:
        el = str(el.text.strip()).replace('\n', 'split').replace('\t', '').split('split')
    while '' in el:
        el.remove('')

    for name in names_from_database:
        if name in el:
            updates.append(el)

for el in updates:
    for i in range(0, len(el)):
        print(el[i] + '\n')
    print('\n' * 3)

print(updates)
