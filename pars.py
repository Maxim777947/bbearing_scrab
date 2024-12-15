from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from func import httml_soup, source_link, next_page, price, price_min
from selenium.webdriver.chrome.options import Options



start = time.perf_counter()
workbook = load_workbook('список.xlsx')
sheet = workbook.active
file_path = 'список.xlsx'  # Укажите путь к вашему файлу
df = pd.read_excel(file_path)
pages_domen = 'https://autopiter.ru/'
sheet['G1'] = 'ссылка'
sheet['H1'] = 'Уточнено'
workbook.save('список.xlsx')
time.sleep(3)
print('Начали')



# Перебор всех строк
for index, row in df.iterrows():
    d =row.to_dict()
    if pd.isna(d['ссылка']):
        artlec = str(d['Артикул']).replace(' ', '%20').replace('/', '%2F').strip()
        page = f'{pages_domen}goods/{artlec}'
        soup = httml_soup(page)
        ass = source_link(soup, d['Бренд'].strip(), str(d['Артикул']).strip())
        if ass is None:
            list_links = next_page(soup)
            if list_links:
                for i in list_links:
                    print('Переходим к след странице по номеру')
                    soup1 = httml_soup(pages_domen + i)
                    ass = source_link(soup1, d['Бренд'], d['Артикул'])
                    if ass:
                        break
        sheet['G' + str(index + 2)] = ass
        str_log = f"{index + 2} добавление ссылки {ass} на подшипник бренда {d['Бренд']}, артикул {d['Артикул']}"
        print(str_log)
        workbook.save('список.xlsx')

workbook.save('список.xlsx')

# https://autopiter.ru/goods/NK%2020%2F20
# https://autopiter.ru/goods/nk%2022%2F20


browser = webdriver.Chrome()




new_price = None
def start2():
    print('НЕ ЗАБУДЬ РАЗВЕРНУТЬ КАРТОЧКУ ТОВАРА')
    for index, row in df.iterrows():
        d =row.to_dict()
        if pd.isna(d['Уточнено']):
            browser.get('https://autopiter.ru' + str(d['ссылка']))
            soup = BeautifulSoup(browser.page_source, "lxml")
            print(index + 2)
            new_price = price(soup)
            price_m = price_min(soup, new_price)
            if new_price is None:
                print('new_price = None нажми я не робот')
                time.sleep(5)
                new_price = price(soup)
            if new_price is not None:
                sheet['H' + str(index + 2)] = new_price
            if price_m:
                if price_m['priceId'] != 30398 or price_m['priceId'] != 32893:
                    red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
                    # Применяем заливку к ячейке
                    sheet['H' + str(index + 2)].fill = red_fill
            print(index + 2, f'обновление цены на {new_price}')
            new_price = None



start2()
workbook.save('список.xlsx')
start2()
workbook.save('список.xlsx')


browser.quit()
finish = time.perf_counter()
print('Время работы: ' + str(finish - start))




# очисти ячеуйк
# разверни карточку товара
# файл должен называться список
# каждая ячейка в столбце в которую будет записывается цена должна быть
#  внутере пустой нажми удалить его чтобы компьютер видел что там ничего нету если в ячеки
#  будет хоть один пробел или она будет закрашена и т.д и тп комп будет думать что там что то есть и не будет в эту ячейку ни чего записыват'' 