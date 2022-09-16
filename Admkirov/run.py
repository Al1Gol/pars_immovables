import re

import requests
from bs4 import BeautifulSoup as bs

from config import *
from to_csv import export_to_csv

def get_link():

    result_data = {
        data_auc_field: [],
        name_field: [],
        cadastr_field: [],
        address_field: [],
        category_field: [],
        type_of_use_field: [],
        area_field: [],
        water_field: [],
        drainage_field: [],
        warm_field: [],
        gas_field: [],
        start_price_field: [],
        last_day_field: [],
        sale_result_field: [],
        note_field: [],
        documents_field: [],
        url_field: []
    }

    for link in links['rent_arenda']:
        i = 1
        response = requests.get(site + link + f'?PAGEN_1={i}')
        print(site+link+f'?PAGEN_1={i}')
        result = response.content
        soup = bs(result, 'lxml')
        table = soup.find('table', class_ = 'table_udms')
        table = table.find('tbody')
        rows = table.find_all('tr')
        for row in rows:  
            columns = row.find_all('td')
            date = columns[0].text.strip()
            result_data[data_auc_field].append(date)  #Добавляем даты

            name = columns[1]

            water = name.find(string='Вода')
            if water:
                water_link = water.parent['href']
                result_data[water_field].append(f'{site}{water_link}') #Вода
            else:
                result_data[water_field].append(f'-') #Вода

            drainage = name.find(string='Водоотведение')
            if drainage:
                drainage_link = drainage.parent['href']
                result_data[drainage_field].append(f'{site}{drainage_link}') #Водоотведение
            else:
                result_data[drainage_field].append(f'-') #Водоотведение

            warm = name.find(string='Тепло')
            if warm:
                warm_link = warm.parent['href']
                result_data[warm_field].append(f'{site}{warm_link}') #Тепло
            else:
                result_data[warm_field].append(f'-') #Тепло

            gas = name.find(string='Газ')
            
            if gas:
                gas_link = gas.parent['href']
                result_data[gas_field].append(f'{site}{gas_link}') #Газ
            else:
                result_data[gas_field].append(f'-') #Тепло

            documents = name.find('ul')
            documents = documents.find_all('li')
            doc_str = ''
            for document in documents:
                doc_url = document.find('a')['href']
                doc_text =  document.find('a').text
                doc_str = doc_str + f'{doc_text} : {site}{doc_url}; '     
            result_data[documents_field].append(doc_str) #Документы
               

            for x in name.select('div'):
                x.decompose()
            for x in name.select('ul'):
                x.decompose()
            name = name.text.strip()
 
            result_data[name_field].append(name) #Добавление наименования

            regex = re.compile('\d{2}:\d{2}:\d+:\d+')
            cadastr = regex.search(name)
            if cadastr:
                cadastr = cadastr[0] #Кадастровый номер
            else:
                cadastr = '-' #Отсутствие кадастрового номера
            
            result_data[cadastr_field].append(cadastr) #Добавление кадастрового номера

            regex = re.compile('[Аа]дрес\s\(описание\sместоположения\):\s?(([А-Я]{2})|([А-Я][а-я]+\s[А-Я][а-я]+),)?\s?[А-Я][а-я]+\.?\s[а-я]+.?,\s(г\.о\.\s)?(г\.|город)\s[А-Я][а-я]+,\s(((г\.)|(город))\s?[А-Я][а-я]+,\s)?[А-Яа-я]*\.?-?[а-я]*\s?[А-Яа-я]+(\s[А-Яа-я]+)?(,\s[а-я]+\.\s[А-Яа-я]*)(,\s[а-я]+\.[0-9]+)?(,\s[0-9]*)')
            address = regex.search(name)
            if address:
                result_data[address_field].append(address[0]) #Адрес
            else:
                result_data[address_field].append('-') #Адрес

            regex = re.compile('[Кк]атегория\sземель\s–\s*[а-я]+\s?[а-я]*\s?[а-я]*\s?[а-я]*')
            category = regex.search(name)
            if category:
                category_res = category[0].split(' – ')
                if len(category_res) == 2:
                    result_data[category_field].append(category_res[1]) #Категория объекта
                else:
                    category_res = category[0].split('–')
                    if len(category_res) == 2:
                        result_data[category_field].append(category_res[1]) #Категория объекта
            else:
                result_data[category_field].append('-') #Категория объекта


            regex = re.compile('[Вв]ид\sразрешенного\sиспользования\s?–\s?[а-я]+\s?[а-я]*\s?[а-я]*\s?[а-я]*')
            type_of_use = regex.search(name)
            if type_of_use:
                type_of_use_res = type_of_use[0].split(' – ')
                if len(type_of_use_res) == 2:
                    result_data[type_of_use_field].append(type_of_use_res[1]) #Тип использования
                else:
                    type_of_use_res = type_of_use[0].split('–')
                    if len(type_of_use_res) == 2:
                        result_data[type_of_use_field].append(type_of_use_res[1]) #Тип использования
            else:
                result_data[type_of_use_field].append('-') #Тип использования
            
            area = columns[2].text.strip()
            result_data[area_field].append(area) #Тип использования

            start_price = columns[3].text.strip()
            result_data[start_price_field].append(start_price) #Начальная цена  

            last_day = columns[4].text.strip()
            result_data[last_day_field].append(last_day) #Последний день подачи заявок 

            res_sale = columns[5].text.strip()
            result_data[sale_result_field].append(res_sale) #Результат продажи

            note = columns[6].text.strip()
            result_data[note_field].append(note) #Примечание

            result_data[url_field].append(f'{site}{link}?PAGEN_1={i}') #Ссылка на объявление      

if __name__ == '__main__':
    get_link()