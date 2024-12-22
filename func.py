import re
import json
import requests
from bs4 import BeautifulSoup



def source_link(soup, brend: str, articul: str):
    '''Ищет ссылку на подшипник по артикулу и конкретному производителю'''
    brend = str(brend).lower()
    if brend == 'китай':
        brend = 'kitaj'
    symbols_to_replace = r"[- /*.]"
    new_articul = re.sub(symbols_to_replace, '', str(articul)).lower().strip(' ')
    
    links = soup.find_all('a')
    urls = [link.get('href') for link in links if link.get('href') is not None]
    for url in urls:
        s = f'{new_articul}/{brend}'
        if s in url:
            return url


def price(soup):
    offer_label = soup.find('span', class_='SelectedOffer__label___3S5Tc', text='Самый дешевый')
    label = soup.find(class_='Notice__inner___3us-1', text='Предложений по запрошенному номеру не найдено')
    if offer_label:
        price_div = offer_label.find_next('div', {'class': 'SelectedOffer__price___3KQqQ'})
        if price_div:
            price_value = int(''.join(price_div.text.strip().split(' ')).strip('\xa0₽')) # Извлекаем только числовое значение
            return price_value
    elif label:
        return 'Предложений по запрошенному номеру не найдено'
    return None


def price_min(soup, price):
    script_tags = soup.find_all('script')

    # Регулярное выражение для поиска JSON-объектов
    json_pattern = re.compile(r'\{.*?\}', re.DOTALL)

    # Список для хранения найденных словарей

    # Извлекаем текст из тегов <script> и ищем словари
    for script in script_tags:
        if script.string:  # Проверяем, есть ли текст внутри тега <script>
            matches = json_pattern.findall(script.string)
            for match in matches:
                try:
                    # Преобразуем строку в словарь
                    dictionary = json.loads(match)
                    if 'detailUid' in dictionary and dictionary['price'] == price:
                        return dictionary
                except json.JSONDecodeError:
                    continue  # Игнорируем ошибки декодирования


def httml_soup(link: str):
    response = requests.get(link)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def next_page(source_link):
    ''' функция выбирает все ссылки следующие по номеру кроме действующей'''
    f = [source_link.find(
        class_='Pagination__page___1ykxs', text=i) for i in range(0, 100)
        ]
    f = list(filter(lambda x: x!=None, map(
        lambda x: x.get('href'), filter(lambda x: x != None, f)))
        )
    return f

