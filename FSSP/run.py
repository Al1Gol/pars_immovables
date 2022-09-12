import re
from tkinter.tix import INTEGER
from config import *
import requests
from bs4 import BeautifulSoup as bs



    
for status in statuses:

    i = 1 #Счетчик пагинации
    empty = '' #Проверка на пустую страницу пагинации

    while True:
        
        params = {
            'torgi[bidnumber]': '',
            'torgi[status]': statuses[status],
            'torgi[torgpublishdate][from]': '',
            'torgi[torgpublishdate][to]': '',
            'torgi[propname]': '',
            'torgi[region]': '4300000000000',
            'torgi[city]': '4300000100000',
            'torgi[propertytype][]': '14',
            'torgi[startprice][from]': '',
            'torgi[startprice][to]': '',
            'torgi[torgexpiredate][from]': '',
            'torgi[torgexpiredate][to]': '',
            'page': f'{i}',
        }
        
        response = requests.get('https://fssp.gov.ru/torgi/ajax_search/', params=params, cookies=cookies, headers=headers)
        result = response.content
        soup = bs(result, 'lxml')
        empty = soup.find('div', class_ = 'empty')

        if empty:
            break

        i = i + 1

        #Получаем все строки с лотами
        regex = re.compile('Лот\s\d+')
        lots_num = soup.find_all(text=regex)
        for lot in lots_num:
            link = lot.find_parent()['href']
            print(link)
    