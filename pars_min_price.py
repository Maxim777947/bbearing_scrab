import time
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl.styles import PatternFill
from openpyxl import load_workbook
from selenium import webdriver
from func import source_price, price_min




workbook = load_workbook('список.xlsx')

sheet = workbook.active

FILE_PATH = 'список.xlsx'

df = pd.read_excel(FILE_PATH)



mehanica = [30398, 32893]

def pars_price():
    '''Основная функция парсит цены и вносит их в таблицу'''
    print('Введите какое количество подшипников нужно проверить?')
    print('Нажмите просто Enter чтобы выполнить всё')
    try:
        counter = int(input())
    except ValueError:
        counter = None
    s = 0

    sheet['H1'] = 'Уточнено'

    browser = webdriver.Chrome()

    for _ in range(5):
        print('НЕ ЗАБУДЬ РАЗВЕРНУТЬ КАРТОЧКУ ТОВАРА')

    for index, row in df.iterrows():
        d =row.to_dict()
        if pd.isna(d['Уточнено']) and pd.notna(d['ссылка']):
            browser.get('https://autopiter.ru' + str(d['ссылка']))
            soup = BeautifulSoup(browser.page_source, "lxml")
            new_price = source_price(soup)
            price_m = price_min(soup, new_price)
            if new_price is None:
                print('new_price = None нажми я не робот')
                time.sleep(3)
            if new_price is not None:
                sheet['H' + str(index + 2)] = new_price
                s += 1
                print(index + 2, f'обновление цены на {new_price}')
            if price_m and new_price:
                if price_m['priceId'] not in mehanica:
                    print('магазин не наш')
                    red_fill = PatternFill(
                        start_color='FF0000',
                        end_color='FF0000',
                        fill_type='solid'
                        )
                    # Применяем заливку к ячейке
                    sheet['H' + str(index + 2)].fill = red_fill
        new_price = None

        if counter:
            if s == counter:
                break
    workbook.save('список.xlsx')

    browser.quit()
