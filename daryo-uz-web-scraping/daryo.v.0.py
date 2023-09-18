from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta
import csv
import re
import pandas as pd 


started_at = datetime.now()
name = 'layfstayl.v.0'
big_url = "https://daryo.uz/category/layfstayl"
#https://daryo.uz/category/maqolalar/?page=48&per-page=10  
header = ['title', 'content', 'time']

url_ignore = "https://daryo.uz/2021/11/02/aktyor-uill-smit-ortiqcha-vazndan-qanday-xalos-bolgani-haqidagi-6-qismli-hujjatli-serialni-suratga-oldi/"
html_text_ignore = requests.get(url_ignore).text 
soup_ignore = BeautifulSoup(html_text_ignore, 'lxml') 
content_ignore = soup_ignore.find("div", class_="default__section border").findAll('p') 
k = content_ignore

def page(big_url):
    for i in range(0, 500):
        response = requests.get(f"{big_url}?page={i}&per-page=10", headers={
                "x-requested-with": "XMLHttpRequest"
        })
        html_text = response.text
        soup = BeautifulSoup(html_text, 'lxml')
        news = soup.find_all('a', class_="mini__article-link")

        if(news):
            for new in news:
                url = f"https://daryo.uz{new['href']}"
                script(url)
                #time.sleep(1)
        else:
            break 
def script(url): 
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
        
    match = re.search(r'\d{4}/\d{2}/\d{2}', url)
    extracted_date = match.group()
    
    try:
        title = soup.find('b').text
        contents = soup.find("div", class_="default__section border").findAll('p')
        c = ''
        for content in contents:
            c+=content.text
            
        writer.writerow([title, c, extracted_date]) 
    except AttributeError:
        url = 'https://daryo.uz/2021/11/02/aktyor-uill-smit-ortiqcha-vazndan-qanday-xalos-bolgani-haqidagi-6-qismli-hujjatli-serialni-suratga-oldi/'
        contents = k
            
with open(f"{name}.csv", 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    page(big_url)
        
finished_at = datetime.now()
print(finished_at-started_at) 
