import time
import asyncio
from pars_link import parse_links, pars_linksssss
from pars_min_price import pars_price

start = time.perf_counter()

print("Ведите:")
print('1 - Запуск поиска ссылок на подшипники и запись их в таблицу Exel ')
print('2 - Запуск поиска ссылок c фильтрацией ')
print('3 - Дособирание ')
print('4 - Запуск поиска минимальной цены и запись в таблицу Exel')


f = int(input())


if f == 1:
    print('Сколько ссылок делаем?')
    try:
        counnter = int(input())
    except:
        counnter = None
    if __name__ == "__main__":
        asyncio.run(parse_links(counnter))

if f == 2:
    print('Сколько ссылок делаем?')
    try:
        counnter = int(input())
    except:
        counnter = None
    if __name__ == "__main__":
        asyncio.run(parse_links(counnter, filter=True))


elif f == 3:
    print('Сколько ссылок делаем?')
    counnter = int(input())
    pars_linksssss(counnter)

elif f == 4:
    pars_price()


finish = time.perf_counter()
print('Время работы: ' + str(finish - start))

