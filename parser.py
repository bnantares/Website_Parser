import requests
import re
import json
from bs4 import BeautifulSoup


URL = 'http://66.vld.msudrf.ru/'
URL_REQUISITES = 'http://66.vld.msudrf.ru/modules.php?name=info_pages&id=1700'
HEADERS = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'accept': '*/*'}
path = './'

requisites_list = {
    'УФК': "(УФК(.*))ИНН",
    'ИНН': "ИНН\D*(\d+)",
    'КПП': "КПП\D*(\d+)",
    'Номер расчетного счета': "Номер расчетного\D*(\d+)",
    'БИК': "БИК\D*(\d+)"
}

def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='info-block')
    
    emplyoees_info_zone = items[0]
    schedule_zone = items[1]

    judge_name = emplyoees_info_zone.find(text=re.compile('([Мм]ировой)')).find_next('b').get_text()
    judge_assistant_name = emplyoees_info_zone.find(text=re.compile('([Пп]омощник)')).find_next('b').get_text()
    secretary_name = emplyoees_info_zone.find(text=re.compile('([Сс]екретарь)')).find_next('b').get_text()
    email = emplyoees_info_zone.find('a').get_text()
    phone_number = [emplyoees_info_zone.find_all('span', class_='right')[1].get_text(strip=True), emplyoees_info_zone.find_all('span', class_='right')[2].get_text(strip=True)]
    schedule = schedule_zone.find(text=re.compile('([Рр]абочие)')).find_next(['ul']).get_text(strip=True)
    citizen_receptions = schedule_zone.find(text=re.compile('([Гг]рафик приема)')).find_next(['ul']).get_text(strip=True)
    launch = schedule_zone.find(text=re.compile('([Оо]бед)')).find_next(['ul']).get_text(strip=True)
    days_off = schedule_zone.find(text=re.compile('([Вв]ыходные)')).find_next(['ul']).get_text(strip=True)

    wonder_list = {
        'ФИО Мирового судьи': judge_name,
        'ФИО Помощника судьи': judge_assistant_name,
        'ФИО Секретаря': secretary_name,
        'Электронная почта': email,
        'Телефон(ы)': phone_number,
        'Рабочие дни': schedule,
        'График приема граждан': citizen_receptions,
        'Обед': launch,
        'Выходные': days_off
    }
    
    return wonder_list

def get_requisites(html):
    new_req = requisites_list
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='outputArea', id='divINFODocText1700')
    for k, v in new_req.items():
    	pattern = re.compile(v)
    	new_req[k] = pattern.search(items.text)[1]
    return new_req

def save_file(data, path):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def parse():
    html = get_html(URL)
    html_requisites = get_html(URL_REQUISITES)
    if html.status_code == 200 and html_requisites.status_code == 200:
        return {**get_content(html.text), **get_requisites(html_requisites.text)}
    else:
        print('<ошибка при загрузке страницы>')

def main():
    parsed_data = parse()
    save_file(parsed_data, path)

if __name__ == '__main__':
    main()