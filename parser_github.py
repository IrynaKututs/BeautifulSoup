import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://minfin.com.ua'            
URL = 'https://minfin.com.ua/cards/'      
a =[]
HEADERS = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

def get_html(url, params = ''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0 jmBHNg')
    for item in items:
        a.append(
            {
                'title': item.find('div', class_="be80pr-15 kwXsZB").get_text(),
                'link_product': HOST + item.find('div', class_="be80pr-9 fJFiLL").find('a').get('href'),
                'brend': item.find('div', class_="be80pr-16 be80pr-17 kpDSWu cxzlon").find('span').get_text(),
                'card_img':item.find('div', class_="be80pr-9 fJFiLL").find('img').get('src')
            }
        )
    return a

def save_doc():
    with open('cards.csv', mode="w",encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(['Название продукта','Cсылка на продукт','Банк','Изображение карты'])
        for item in a:
            writer.writerow([item['title'],item['link_product'],item['brend'],item['card_img']])

def parser():
    html = get_html(URL)
    print(get_content(html.text))
    save_doc()

parser()