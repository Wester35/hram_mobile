import aiohttp
import asyncio
import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

date_now = datetime.date.today()
date_now = str(date_now)[:7]
path = f'images/{date_now}.jpg'
url_for_image = 'https://www.hramalnevskogo.ru/page40966859.html'
url_to_parse = 'https://www.hramalnevskogo.ru/page41137881.html'
list_for_urls = []


def get_fake_user_agent():
    ua = UserAgent()
    return ua.random


async def download_image(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_content = await response.read()
            with open(save_path, 'wb') as file:
                file.write(image_content)
            print(f"Image downloaded successfully and saved at: {save_path}")


async def parse_html_img():
    headers = {'User-Agent': get_fake_user_agent()}
    async with aiohttp.ClientSession() as session:
        async with session.get(url_for_image, headers=headers) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                img_adr = soup.find('img')
                img_url = img_adr['data-original']
                await download_image(img_url, path)
            else:
                print(f"Failed to retrieve the page. Status code: {response.status}")


async def parse_html(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        # Устанавливаем User-Agent
        user_agent = get_fake_user_agent()
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

        driver.get(url)
        if options.headless:
            print("Chrome запущен в headless режиме.")
        else:
            print("Chrome запущен в обычном режиме с интерфейсом.")

        await asyncio.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        li_obj = soup.find_all('li',
                               class_='js-feed-post t-feed__post t-item t-width t-feed__grid-col t-col t-col_3 t-align_left')
        for div in li_obj:
            list_for_urls.append(div.a['href'])

        print(list_for_urls)

        # pars everyone urls###########################################################
        for _url in list_for_urls:
            driver.get(_url)
            filename = _url.split('/')[-1]
            _soup = BeautifulSoup(driver.page_source, 'html.parser')
            div_object = _soup.find('div', class_='t-feed__post-popup__content t-col t-col_8')
            with open(f'webpages/{filename}.html', "w", encoding='utf-8') as file:
                file.write(str(div_object))

    except Exception as e:
        print(f"Error parsing HTML: {e}")
    finally:
        driver.quit()


async def start():
    task1 = asyncio.create_task(parse_html(url_to_parse))
    task2 = asyncio.create_task(parse_html_img())
    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    asyncio.run(start())
