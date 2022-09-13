import re

import requests
from bs4 import BeautifulSoup as bs

from config import *

test_link = '?notificationId=134501&lotId=596227'

def get_data(url):
    response = requests.get(url)
    result = response.content
    soup = bs(result, 'lxml')

    address = soup.find(string='Детальное местоположение:').parent
    address = address.find_next_sibling('td').text      #Адрес
    
    price = soup.find(string='Начальная цена:').parent
    price = price.find_next_sibling('td').text #Цена

    organizer = soup.find(string='Организатор торгов:').parent
    organizer = organizer.find_next_sibling('td')
    organizer = organizer.find(string='подробнее').parent.previous.strip() #Организатор

    name = soup.find(string='Наименование и характеристика имущества:').parent
    name = name.find_next_sibling('td').text   #Наименование и описание
    
    #Назначением объекта

    regex = re.compile('авп\d*\s*\d+\.?\,?\d*\s*кв\.м\.')
    area = regex.search(name)
    if area:
        area = area[0] #Площадь
    else:
        area = '-' #Отстутсвие площади

    regex = re.compile('\d{2}:\d{2}:\d+:\d+')
    cadastr = regex.search(name)
    if cadastr:
        cadastr = cadastr[0] #Кадастровый номер
    else:
        cadastr = '-' #Отсутствие кадастрового номера
    
    encumbrance = soup.find(string='Обременение:').parent

    if encumbrance:
        encumbrance = encumbrance.find_next_sibling('td').text #Наличие обременения
    else:
        encumbrance = '-' #Отсутствие обременения

    descr_encum = soup.find(string='Описание обременения:').parent

    if descr_encum:
        descr_encum = descr_encum.find_next_sibling('td').text #Описание обременения
    else:
        descr_encum = '-' #Отсутствие описания обременения

    regex_fio = re.compile('[А-Я][а-я]+\s?[А-Я]\.+\s?[А-Я]\.')
    regex_fio_full = re.compile('[А-Я][а-я]+\s[А-Я][а-я]+\s[А-Я][а-я]+\s')

    fio = regex_fio.search(name)
    fio_full = regex_fio_full.search(name)

    if fio:
        owner = fio[0] #Собственник
    elif fio_full:
        owner = fio_full[0] #Собственник
    else:
        owner = '-' #Отсутствует собственник
    
    regex = re.compile('[В,в]ид права:[^\.]+\.')
    type_of_law = regex.search(name)
    if type_of_law:
        type_of_law = type_of_law[0].split(':')[1][:-1] #Вид права
    else:
        type_of_law = '-' #Отсутствует вид права

    start = soup.find(string='Дата начала подачи заявок:').parent  
    start = start.find_next_sibling('td').text  #Дата начала подачи заявок

    finish = soup.find(string='Дата окончания подачи заявок:').parent  
    finish = finish.find_next_sibling('td').text #Дата окончания подачи заявок

    status = soup.find(string='Статус:').parent  
    status = status.find_next_sibling('td').text #Статус

    subject = soup.find(string='Предмет торга:').parent  
    subject = subject.find_next_sibling('td').text #Предмет торга

    type_of_property = soup.find(string='Вид имущества:').parent  
    type_of_property = type_of_property.find_next_sibling('td').text #Тип собственности

    result = {
        'address': address,
        'price': price,
        'organizer': organizer,
        'name': name,
        'area': area,
        'cadastr': cadastr,
        'encumbrance': encumbrance,
        'descr_encum': descr_encum,
        'owner': owner,
        'type_of_law': type_of_law,
        'start': start,
        'finish': finish,
        'status': status,
        'subject': subject,
        'type_of_property': type_of_property  
    }

    return result

if __name__ == '__main__':
    get_data(site+test_link)