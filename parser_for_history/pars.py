import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

path = 'pngg/image.jpg'


def get_fake_user_agent():
    ua = UserAgent()
    return ua.random


def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully and saved at: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")


def parse_html(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        li_obj = soup.find_all('li', class_='js-feed-post t-feed__post t-item t-width t-feed__grid-col t-col t-col_3 t-align_left')
        #div_obj = soup.find_all('div', class_='js-feed-post-title t-feed__post-title  t-name t-name_xs')
        for div in li_obj:
            # в разработке
            #div_block = div.find('div', class_='t-feed__post-bgimg t-bgimg loaded'))
            print(div.a['href'])
        #print(li_obj)
    except Exception as e:
        print(f"Error parsing HTML: {e}")
    finally:
        driver.quit()


url_to_parse = 'https://www.hramalnevskogo.ru/page41137881.html'
parse_html(url_to_parse)