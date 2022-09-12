import requests
import re
from bs4 import BeautifulSoup as bs

from config import *
from urls_parsing import get_links


#Проходим по страницам лотов и собираем информацию
def get_data():
    
    result_data = {
        region_field: [],
        type_auction_field: [],
        price_field: [],
        type_of_object_field: [],
        address_field: [],
        area_field: [],
        contacts_field: [],
        documents_field: [],
        presentation_field: [],
        decript_field: [],
        cadastr_field: [],
        link_field: []
    }
    data_of_lot = []
    links = get_links()

    for link in links:
        url = f'{site}{link[1]}'
        direct_sale = (link[2] == 'Прямая продажа') or (link[2] == 'Готовится к продаже')

        result_data[region_field].append(link[0]) #Добавляем регион

        req = requests.get(url)
        result = req.content.decode('utf-8')
        soup = bs(result, 'lxml')
        if direct_sale:
            result_data[type_auction_field].append(link[2]) #Добавляем способ продажи
        else:
            auction_data = soup.find('div', class_ = 'element-data')
            type_auction = auction_data.find('dt', text='Тип торгов:')
            type_auction = type_auction.find_next().text
 
            result_data[type_auction_field].append(type_auction) #Добавляем способ продажи

        price = soup.find('div', class_ = 'element-buyout')
        price = price.find('dd')
        if price:
            price = price.text
            result_data[price_field].append(price) #Добавляем стоимость
        else:  
            result_data[price_field].append('Отсутствует') #Добавляем стоимость
        

        if direct_sale:
            result_data[type_of_object_field].append('Земельный участок')
        else:
            link_of_auction = soup.find('a', class_ = 'js-ajax-toggle')['data-href']
            req = requests.get(f'{site}{link_of_auction}')
            result = req.content.decode('utf-8')
            soup_auction = bs(result, 'lxml')
            type_of_object = soup_auction.find('span', text='Вид объекта:')
            type_of_object = type_of_object.find_next().text

            result_data[type_of_object_field].append(type_of_object) #Добавляем вид объекта
        
        address = soup.find('a', href='#mapDialog').text

        result_data[address_field].append(address) #Добавляем адрес
        area = soup.find('div', class_='element-infoparams')
        area = area.find('dt', text='Общая площадь ЗУ')
        if area:
            area = area.find_next().text
            result_data[area_field].append(area) #Добавляем площадь
        else:
            result_data[area_field].append(f'отсутсвует') #Если отстутствует

        manager = soup.find('div', class_='element-contact')
        manager = manager.find('dd')
        manager_name = manager.find('div', class_='element-contact__name')
        manager_phone = manager_name.find_next().text
        manager_name = manager_name.text

        result_data[contacts_field].append(f'ФИО: {manager_name}, тел:{manager_phone}') #Добавляем контакты менеджера

        documents = soup.find('a', class_='download-link')
        if documents:
            documents = documents['href']
            result_data[documents_field].append(f'{site}{documents}') #Добавление ссылки на документы
        else:
            result_data[documents_field].append(f'отсутсвует')#Если отстутствует

        presentation = soup.find(text='Презентация')
        if presentation:
            presentation = presentation.find_parent('a')['href']
            result_data[presentation_field].append(f'{site}{presentation}') #Добавление презентации
        else:
            result_data[presentation_field].append(' ') #Если отсутствует - добавляем пустую строку

        description = soup.find('div', class_='descr-block')
        description = description.find_all('p')
        str_res = ''
        for line in description:
            str_res = str_res + line.text    
        result_data[decript_field].append(str_res) #Добавление описания

        regex = re.compile('\d{2}:\d{2}:\d+:\d+')
        cadastr = regex.search(str_res)
        if cadastr:
            result_data[cadastr_field].append(cadastr.group(0)) #Добавляем кадастровый номер
        else:
            result_data[cadastr_field].append('остутствует') #Если отстутствует
        result_data[link_field].append(f'{site}{link[1]}') #Добавляем ссылку на лот

    print('Получение данных завершено.')

    return result_data 
        
if __name__ == '__main__':
    get_data()

