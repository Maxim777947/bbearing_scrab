import pandas as pd
from openpyxl import load_workbook

from func import httml_soup, source_link, next_page



pages_domen = 'https://autopiter.ru/'

workbook = load_workbook('список.xlsx')

file_path = 'список.xlsx'

sheet = workbook.active


df = pd.read_excel(file_path)


def pars_links():
    print('Введите какое количество ссылок нужно создать?')
    print('Нажмите просто Enter чтобы выполнить всё')

    try:
        counter = int(input())
    except ValueError:
        counter = None

    sheet['G1'] = 'ссылка'

    workbook.save('список.xlsx')

    s = 0
    # Перебор всех строк в exel
    for index, row in df.iterrows():
        d =row.to_dict()
        if pd.isna(d['ссылка']):
            artlec = str(d['Артикул']).replace(' ', '%20').replace('/', '%2F').strip()
            page = f'{pages_domen}goods/{artlec}'
            soup = httml_soup(page)
            #получаем ссылку на интересующий нас подшипник
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
            if ass:
                sheet['G' + str(index + 2)] = ass
                str_log = f"{index + 2} добавление ссылки {ass} на подшипник бренда {d['Бренд']}, артикул {d['Артикул']}"
                print(str_log)
                s += 1
        if index % 10 == 0:
            workbook.save('список.xlsx')
        if counter:
            if s == counter:
                break

    workbook.save('список.xlsx')