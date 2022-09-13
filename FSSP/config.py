site = 'https://fssp.gov.ru/torgi/'

statuses = {
    'active': '7',
    'announced': '5'
}

cities = [
    {
        'region': {
            'Kirovskiy': 4300000000000  
        },
        'city': {
            'Kirov': 4300000100000
        }
    }
]

cookies = {
    'sp_test': '1',
    'PHPSESSID': 'i7uqep4ss5u3ilmbs6h1qtvbe3',
    'sputnik_session': '1662980108312|4',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'sp_test=1; PHPSESSID=i7uqep4ss5u3ilmbs6h1qtvbe3; sputnik_session=1662980108312|4',
    'Referer': 'https://fssp.gov.ru/torgi/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


address_field = 'Адрес'
price_field = 'Цена'
organizer_field = 'Организатор'
name_field = 'Номер лота/Описние'
area_field = 'Площадь'
cadastr_field = 'Кадастровый номер'
encumbrance_field = 'Обременение'
descr_encum_field = 'Описание обременения'
owner_field = 'Собственник'
type_of_law_field = 'Вид права'
start_field = 'Начало торгов'
finish_field = 'Окончание торгов'
status_field = 'Статус'
subject_field = 'Предмет торга'
type_of_property_field = 'Тип собственности' 
link_field = 'Ссылка'
