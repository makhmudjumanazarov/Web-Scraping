from bs4 import BeautifulSoup
import requests

import csv


big_url = input('Linkni kiriting>>> ')
n = int(input('Nechta sahifani olishni xohlaysiz?(har bir sahifada 30 ta yangilik bor)>>>'))
name = input('Dataframega nom bering:>>>')
header = ['title', 'content']

def script(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    title = soup.find('div', class_="single-header__title").text
    contents = soup.find_all('p')
    c = ''
    for content in contents:
        c+=content.text
    writer.writerow([title, c])


def page(big_url):
    html_text = requests.get(big_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('a', class_ = "news__title")

    for new in news:
        url = f"https://kun.uz{new['href']}"
        script(url)
    return soup.find('a', class_ = "load-more__link")['href']

with open(f"{name}.csv", 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(n):
        b = page(big_url)
        big_url = f"https://kun.uz{b}"




