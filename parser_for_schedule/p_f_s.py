# import requests
# from bs4 import BeautifulSoup
#
# link1 = 'https://www.hramalnevskogo.ru/page40966859.html'
#
# html_content = requests.get(link1).text
#
# # Инициализация объекта BeautifulSoup для парсинга HTML
# soup = BeautifulSoup(html_content, 'html.parser')
#
# # Извлечение ссылки из атрибута 'content' тега 'meta' с атрибутом 'itemprop="image"'
# img_tag = soup.find('img')
#
# # for img in img_tag:
# #     print(img.get('src'))
#
# if img_tag:
#     link = img_tag.get('src')
#     print("Найденная ссылка:", link)
# else:
#     print("Ссылка не найдена.")


#########
from time import sleep
import requests
from bs4 import BeautifulSoup

link = 'https://www.hramalnevskogo.ru/page40966859.html'

html_content = requests.get(link).text
sleep(0.1)
# Инициализация объекта BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html_content, 'html.parser')
sleep(0.1)
# Извлечение ссылки из атрибута 'src' тега 'img'
img_tag = soup.find('img')
sleep(0.1)
link = img_tag.get('src')
sleep(0.1)
print("Найденная ссылка:", link)
