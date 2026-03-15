import requests
from lxml import etree


#Подключаемся к сайту и записываем результат в url
url = requests.get('https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml?iss.dp=comma&iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST')
#Переводим текстовую строку в объект
tree = etree.fromstring(url.content)

#Ищем подходящие элементы в html, в данном случае нас интересует элемент row
rows = tree.xpath("//row")

#Список моих компаний, по которым я буду фильтровать полученный результат
my_stocks = ['AQUA', 'CHMF', 'SBER', 'MOEX', 'LKOH', 
             'X5', 'IRAO', 'SIBN', 'POSI', 'MAGN', 'NLMK', 
             'NVTK', 'SOFL', 'SNGSP', 'YDEX', 'T', 'TTLK', 
             'TATN', 'RAGR']

#Пустой словарь для значений
stocks_and_prices = {}


for row in rows:
    #Ищем элементы row с загодовками SECID и LAST, для нас это тикер и цена
    name = row.get('SECID')
    price = row.get('LAST')

    #С помощью данной конструкции проверяем, есть ли цена у тикера, а также заменяем "," на ".". Это позволит перевест истроку во float. 
    if price:
        price = price.replace('.', ',')
        if ',' in price:
            stocks_and_prices[name] = price
        #Здесь добавляется в конец два нуля, если цена как целое число.
        else:
            price = price + ',00'
            stocks_and_prices[name] = price
    #Если нету цены, то идём дальше
    else:
        continue

#Создаём будущий словарь, куда будем заносить только те компании, которые ест ьв словаре my_stocks
clear_dict = {}
#Создаём и открывваем новый файл csv
with open('market_stocks.csv', 'w', encoding='utf-8') as file:
    file.write('Тикер;Цена\n')
    #Пробегаемся по списку компаний, сопоставляя с ключами в словаре stocks_and_prices
    for ticker in my_stocks:
        if ticker in stocks_and_prices:
            #Найдя ту самую компанию, берём её цену и записываем в новый словарь как значение
            total_price = stocks_and_prices[ticker]
            clear_dict[ticker] = total_price
        #Если не та компания, идём дальше
        else:
            continue
    #Формируем словарь в переменную, чтобы записать её в файл csv с помощью цикла
    for name, price in clear_dict.items():
        result = '{}; {}\n'.format(name, price)
        file.write(result)

print("Данные обновлены!")
