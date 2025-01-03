import pandas as pd
import asyncio
import aiohttp
import time
from openpyxl import load_workbook
from bs4 import BeautifulSoup
from func import httml_soup, source_link, next_page


pages_domen = 'https://autopiter.ru/'

file_path = 'список.xlsx'


async def fetch(session, index, url, brend, art, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, 'html.parser')
            ass = source_link(soup, brend, art)
            ss = (index + 2, ass)
            print(f"Найдена ссылка {ss}")
            return ss                     


async def parse_links():

    workbook = load_workbook('список.xlsx')

    sheet = workbook.active

    df = pd.read_excel(file_path)

    semaphore = asyncio.Semaphore(10)

    async with aiohttp.ClientSession() as session:

        tasks = []
        
        for index, row in df.iterrows():
            d = row.to_dict()
            if pd.isna(d['ссылка']):
                artlec = str(d['Артикул']).replace(' ', '%20').replace('/', '%2F').strip()
                page = f'{pages_domen}goods/{artlec}'
                tasks.append(fetch(session, index, page, d['Бренд'], d['Артикул'], semaphore))

        # Выполняем все задачи асинхронно
        responses = await asyncio.gather(*tasks)

        # Обработка ответов
        for i in responses:
            if i[1]:
                sheet['G' + str(i[0])] = i[1]
                str_log = f"{i[0]} добавление ссылки {i[1]} в таблицу"
                print(str_log)
        
        workbook.save('список.xlsx')



def pars_linksssss():

    workbook = load_workbook('список.xlsx')

    sheet = workbook.active

    df = pd.read_excel(file_path)
    
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

    workbook.save('список.xlsx')