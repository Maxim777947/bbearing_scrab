import re
import json
import requests
from bs4 import BeautifulSoup

def replace_article(article):
    artlec = str(article
                    ).lower(
                    ).replace(' ', '%20'
                    ).replace('/', '%2F'
                    ).replace(',', '%2C'
                    ).replace('шсп', '%2C'
                    ).strip()
                
    return artlec
    
    
def replace_brend(brend):
    brend = str(brend
                ).lower(
                ).replace('вмпавто', 'vmpavto'
                ).replace('сервис-ключ', 'servis-klyuch'
                ).replace('китай', 'kitaj'
                ).replace('россия', 'rossiya'
                ).replace('app-group', 'app-grupp'
                ).replace('спз', 'spz'
                ).replace('гпз', 'gpz'
                ).replace('л', 'l'
                ).replace('к', 'k'
                ).replace('м', 'm'
                ).strip(' '
                )
    return brend


def replace_article_url(article):
    ''' Функция для формироватия артикля в url '''
    symbols_to_replace = r"[- /*.,()]"
    new_articul = re.sub(symbols_to_replace, '', str(article)).lower().strip(' ')

    artlec = new_articul.lower(
                    ).replace('шсп', 'scp'
                    ).replace('шсл', 'scl'
                    ).replace('л', 'l'
                    ).replace('е', 'e'
                    ).replace('а', 'a'
                    ).replace('м', 'm'
                    ).replace('с', 'c'
                    ).strip()
                
    return artlec


def source_link(soup, brend: str, articul: str):
    '''Ищет ссылку на подшипник по артикулу и конкретному производителю'''
    brend = replace_brend(brend)
    # symbols_to_replace = r"[- /*.,()]"
    new_articul = replace_article_url(articul)
    # print(new_articul)
    # print(brend)
    links = soup.find_all('a')
    urls = [link.get('href') for link in links if link.get('href') is not None]
    for url in urls:
        s = f'{new_articul}/{brend}'
        if s in url:
            return url
    return None


def source_price(soup):
    '''Функция ищет минимальную цену на странице или её отсутствие'''
    offer_label = soup.find('span', class_='SelectedOffer__label___3S5Tc', text='Самый дешевый')
    label = soup.find(
        class_='NonRetailAppraisePricesTab__notice___3_Psa',
        text='Предложений по запрошенному номеру не найдено'
        )
    if offer_label:
        price_div = offer_label.find_next('div', {'class': 'SelectedOffer__price___3KQqQ'})
        if price_div:
            # Извлекаем только числовое значение
            price_value = int(''.join(price_div.text.strip().split(' ')).strip('\xa0₽'))
            return price_value
    elif label:
        return 'Предложений по запрошенному номеру не найдено'
    return None


def price_min(soup, price):
    '''Функция ищет первого продавца в таблице'''
    script_tags = soup.find_all('script')

    # Регулярное выражение для поиска JSON-объектов
    json_pattern = re.compile(r'\{.*?\}', re.DOTALL)

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
    return None


def httml_soup(link: str, timeout: int = 10):
    '''Функция возвращает объект BeautifulSoup'''
    try:
        response = requests.get(link, timeout=timeout)
        response.raise_for_status()  # Вызывает HTTPError для плохих ответов
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    except requests.exceptions.Timeout:
        print(f"Запрос к {link} истек по времени после {timeout} секунд.")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка: {e}")


def next_page(source_links):
    ''' функция выбирает все ссылки следующие по номеру кроме действующей'''
    f = [source_links.find(
        class_='Pagination__page___1ykxs', text=i) for i in range(0, 100)
        ]
    f = list(filter(lambda x: x is not None, map(
        lambda x: x.get('href'), filter(lambda x: x is not None, f)))
        )
    return f
