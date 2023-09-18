from bs4 import BeautifulSoup
import requests
import pandas as pd 
import csv
import re

big_url = 'https://kun.uz/uz/news/category/iktisodiet'
name = 'iqtisodiyot'
header = ['title', 'description', 'content', 'time']


def script(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    title = soup.find('h1', class_="single-header__title").text
    
    description = soup.find_all('h4')
    c = ''
    for desc in description:
        c+=desc.text
    
    content = soup.find_all('p')
    k = ''
    for con in content:
        k+=con.text
        
    match = re.search(r'\d{4}/\d{2}/\d{2}', url)
    extracted_date = match.group()
    
    writer.writerow([title, c, k, extracted_date])

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
    
    while big_url:
        b = page(big_url)
        big_url = f"https://kun.uz{b}"
