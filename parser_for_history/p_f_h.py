import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
    headers = {
        'User-Agent': get_fake_user_agent(),
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        li_obj = soup.find_all('div', class_='t-feed__col-grid__post-wrapper')
        print(li_obj)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


url_to_parse = 'https://www.hramalnevskogo.ru/page41137881.html'

parse_html(url_to_parse)
