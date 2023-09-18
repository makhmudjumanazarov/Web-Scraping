from bs4 import BeautifulSoup
import requests
import pandas as pd 
import csv
import re

pages = []
with open('uzbekiston.txt') as f:
    lines =  f.readlines()
    for i in range(len(lines)):
        pages.append(lines[i][0:-1])
        
name = 'uzbekiston_2'
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

with open(f"{name}.csv", 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for i in range(796, len(pages)):    
        html_text = requests.get(pages[i]).text
        soup = BeautifulSoup(html_text, 'lxml')
        news = soup.find_all('a', class_ = "news__title")
        for new in news:
            url = f"https://kun.uz{new['href']}"
            script(url)
