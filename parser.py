import requests
import shelve
from bs4 import BeautifulSoup
import functions
import re

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"


def parse():
    """
    Парсит названия анекдотов с сайта
    """
    global user_agent
    headers = {
        "accept": "*/*",
        "user-agent": user_agent
    }

    req = requests.get(f"https://www.native-english.ru/jokes", headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    categories_data = soup.find_all(['div'], {"class": ["stack__primary"]})
    products_data = functions.create_formated_list(categories_data, True)
    with shelve.open('categories.db') as db:
        for product in products_data:
            req = requests.get(f"https://www.native-english.ru/jokes/category/{product}", headers=headers)
            src = req.text
            soup = BeautifulSoup(src, "lxml")
            jokes = soup.find_all(['ul'], {"class": ["list list_big"]})
            joke_list = functions.create_formated_list(jokes, False)
            db[product] = joke_list


def give_joke(joke):
    """
    Возвращает текст анекдота
    :param joke: Название анекдота
    """
    global user_agent
    headers = {
        "accept": "*/*",
        "user-agent": user_agent
    }
    url = 'https://www.native-english.ru/jokes/' + joke.replace("'", '')
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    content = soup.find_all(['h1', 'div'], {"class": ["title", 'article']})
    text = f"*{content[0].get_text()}* \n\n"
    for i in range(1, len(content)):
        text += re.sub(r'[_]+', '\n', f'`{content[i].get_text()}`'.replace("  ", "_") + '\n')
    return text
