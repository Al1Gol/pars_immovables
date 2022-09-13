import re

import requests
from bs4 import BeautifulSoup as bs

from config import *
from get_data import get_data
from to_csv import export_to_csv


#Пока только по Кирову
def get_links():    

    result_data = {
        address_field: [],
        price_field: [],
        organizer_field: [],
        name_field: [],
        area_field: [],
        cadastr_field: [],
        encumbrance_field: [],
        descr_encum_field: [],
        owner_field: [],
        type_of_law_field: [],
        start_field: [],
        finish_field: [],
        status_field: [],
        subject_field: [],
        type_of_property_field: [], 
        link_field: [],
    }
    
    for region in regions:
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
                    'torgi[region]': region[0],
                    'torgi[city]': region[1],
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
                    link = site + lot.find_parent()['href']
                    data = get_data(link)
                    result_data[address_field].append(data['address'])
                    result_data[price_field].append(data['price'])
                    result_data[organizer_field].append(data['organizer'])
                    result_data[name_field].append(data['name'])
                    result_data[area_field].append(data['area'])
                    result_data[cadastr_field].append(data['cadastr'])
                    result_data[encumbrance_field].append(data['encumbrance'])
                    result_data[descr_encum_field].append(data['descr_encum'])
                    result_data[owner_field].append(data['owner'])
                    result_data[type_of_law_field].append(data['type_of_law'])
                    result_data[start_field].append(data['start'])
                    result_data[finish_field].append(data['finish'])
                    result_data[status_field].append(data['status'])
                    result_data[subject_field].append(data['subject'])
                    result_data[type_of_property_field].append(data['type_of_property'])
                    result_data[link_field].append(link)

    export_to_csv(result_data)



if __name__ == '__main__':
    get_links()