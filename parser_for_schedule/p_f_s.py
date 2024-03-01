# import requests
# from bs4 import BeautifulSoup
# from time import sleep
# link1 = 'https://www.hramalnevskogo.ru/page40966859.html'
# #sleep(1)
# html_content = requests.get(link1).text
# #sleep(2)
# # Инициализация объекта BeautifulSoup для парсинга HTML
# soup = BeautifulSoup(html_content, 'html.parser')
# #sleep(2)
# # Извлечение ссылки из атрибута 'content' тега 'meta' с атрибутом 'itemprop="image"'
# img_tag = soup.find('meta', 'itemprop="image"')
#
# # for img in img_tag:
# #     print(img.get('src'))
#
# if img_tag:
#     link = img_tag.get('content')
#     print("Найденная ссылка:", link)
# else:
#     print("Ссылка не найдена.")


#########
from time import sleep
import requests
from bs4 import BeautifulSoup

link1 = 'https://www.hramalnevskogo.ru/page40966859.html'


while True:
    html_content = requests.get(link1).text
    sleep(2)
    soup = BeautifulSoup(html_content, 'html.parser')

    img_tag = soup.find('img', class_='t-img t-width t107__widthauto loaded')

    if img_tag:
        sleep(0.1)
        link = img_tag.get('src')
        sleep(0.1)
        print("Найденная ссылка:", link)
        break
    else:
        print(f"Ссылка не найдена. []")
