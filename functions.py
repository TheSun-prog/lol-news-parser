import requests
from bs4 import BeautifulSoup as BS
import sqlite3


def beggining():
    while True:
        menu_text = """
        0 - Leave programm
        1 - Start program
        2 - Update all info
        """
        match input(menu_text):
            case '0': exit()
            case '1': break
            case '2':
                update_all_hero_names()
                update_all_skills_names()
                print('All informations was updated')


def update_all_hero_names():
    r = requests.get('https://www.leagueoflegends.com/ru-ru/champions/?_gl=1*1jhskv4*_ga*MTEyNzk2MTk5MC4xNjQxMDM1MzU3*_ga_FXBJE5DEDD*MTY0Nzc2NTYyNi4xMC4xLjE2NDc3NjcxMDQuNDA.')
    hero_names_html = BS(r.content, 'lxml').find('div', class_="style__List-sc-13btjky-2 dLJiol")
    hero_names_from_html = [x.text for x in hero_names_html]

    con = sqlite3.connect('lol.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS hero_names(id BIGINT, name TEXT)')
    database_id = cur.execute('SELECT id FROM hero_names').fetchall()
    database_names = cur.execute('SELECT name FROM hero_names').fetchall()

    ids_from_database = []
    names_from_database = []
    for el in database_id:
        ids_from_database.append(el[0])
    for el in database_names:
        names_from_database.append(el[0])

    if len(ids_from_database) != 0:
        id = ids_from_database[-1] + 1
    else:
        id = 0

    for el in hero_names_from_html:
        if el not in names_from_database:
            cur.execute('INSERT INTO hero_names VALUES(?, ?)', (id, el))
            id += 1
    con.commit()
    con.close()
    print('its working')


def update_all_skills_names():
    r = requests.get('https://leagueoflegends.fandom.com/ru/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%87%D0%B5%D0%BC%D0%BF%D0%B8%D0%BE%D0%BD%D0%BE%D0%B2')
    heroes_url_html = BS(r.content, 'lxml').find('tbody').find_all('tr')
    for i in range(0, 1):
        heroes_url_html.pop(0)

    heroes_url = []
    for el in heroes_url_html:
        heroes_url.append('https://leagueoflegends.fandom.com' + el.find('a').get('href'))

    con = sqlite3.connect('lol.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS skill_names(id INT, passive TEXT, q TEXT, w TEXT, e TEXT, r TEXT)""")
    con.commit()
    con.close()

    for url in heroes_url:
        r = requests.get(url)
        skill_names_html = BS(r.content, 'lxml')
        passive_name = skill_names_html.find('div', class_="skill skill_innate").find('td').text
        q_name = skill_names_html.find('div', class_="skill skill_q").find('td').text
        w_name = skill_names_html.find('div', class_="skill skill_w").find('td').text
        e_name = skill_names_html.find('div', class_="skill skill_e").find('td').text
        r_name = skill_names_html.find('div', class_="skill skill_r").find('td').text
