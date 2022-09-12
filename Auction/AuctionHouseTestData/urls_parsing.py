import requests
from bs4 import BeautifulSoup as bs
from config import *


#Сбор ссылок лотов, удовлетворяющих по требованиям
def get_links():

    links_of_lots = []

    for city in cities:
        url = f'{site}/catalog/category/land_plots_buildings/region/{cities[city]}/' #area_from/5000/'
        req = requests.get(url)
        result = req.content.decode('utf-8')
        soup = bs(result, 'lxml')
        lots = soup.find_all('div', class_ = 'span3 elements-item')
        for lot in lots:
            descript = lot.find_all('li')
            address = (descript[0].find('span', class_ = 'elements-propval')['title'])
            #if ((address.find(f'г. {city}') > 0) or (address.find(f'г.{city}') > 0)):
            link = lot.find('div', class_ = 'elements-image')
            link = link.find('a')['href']
            type_of_sale = lot.find('div', class_ = 'card-info')
            type_of_sale = type_of_sale.find('a', class_ = 'rollover info').text.strip()
            links_of_lots.append([city, link, type_of_sale]) 
    print(f'Найдено {len(links_of_lots)} позиций')

    return links_of_lots


if __name__ == '__main__':
    get_links() 