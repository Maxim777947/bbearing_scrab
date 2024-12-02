from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import requests
from openpyxl import load_workbook
import re



start = time.perf_counter()
workbook = load_workbook('список.xlsx')
sheet = workbook.active
file_path = 'список.xlsx'  # Укажите путь к вашему файлу
df = pd.read_excel(file_path)
pages_domen = 'https://autopiter.ru/'


def source_link(soup, brend: str, articul: str):
    '''Ищет ссылку на подшипник по артикулу и конкретному производителю'''
    brend = str(brend).lower()
    symbols_to_replace = r"[- ]"
    new_articul = re.sub(symbols_to_replace, '', str(articul)).lower()
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


def httml_soup(link: str):
    response = requests.get(link)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def next_page(source_link):
    ''' функция выбирает все ссылки следующие по номеру кроме действующей'''
    f = [source_link.find(class_='Pagination__page___1ykxs', text=i) for i in range(0, 100)]
    f = list(filter(lambda x: x!=None, map(lambda x: x.get('href'), filter(lambda x: x != None, f))))
    return f


# Перебор всех строк
for index, row in df.iterrows():
    d =row.to_dict()
    if pd.isna(d['ссылка']):
        page = f'{pages_domen}goods/{str(d['Артикул']).replace(' ', '%20')}'
        soup = httml_soup(page)
        ass = source_link(soup, d['Бренд'], d['Артикул'])
        if ass is None:
            list_links = next_page(soup)
            if list_links:
                for i in list_links:
                    print('Переходим к след странице по номеру')
                    soup1 = httml_soup(pages_domen + i)
                    ass = source_link(soup1, d['Бренд'], d['Артикул'])
                    if ass:
                        break
        sheet['F' + str(index + 2)] = ass
        print(index + 2, 'добавление ссылки', ass)
        workbook.save('список.xlsx')



browser = webdriver.Chrome()



new_price = None

for index, row in df.iterrows():
    d =row.to_dict()
    browser.get('https://autopiter.ru' + str(d['ссылка']))
    soup = BeautifulSoup(browser.page_source, "lxml")
    if pd.isna(d['Уточнено']):
        new_price = price(soup)
        if new_price is None:
            print('new_price = None нажми я не робот')
            time.sleep(5)
            new_price = price(soup)
        sheet['G' + str(index + 2)] = new_price
        workbook.save('список.xlsx')
        print(index + 2, f'обновление цены на {new_price}')
        new_price = None





workbook.save('список.xlsx')
browser.quit()
finish = time.perf_counter()
print('Время работы: ' + str(finish - start))
