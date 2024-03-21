import aiohttp
import asyncio
import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json


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

        # pars every urls###########################################################
        for _url in list_for_urls:
            driver.get(_url)
            filename = _url.split('/')[-1]
            _soup = BeautifulSoup(driver.page_source, 'html.parser')
            div_object = _soup.find('div', class_='t-feed__post-popup__content t-col t-col_8')
            div_image = div_object.find_all('div', class_='t-slds__bgimg t-bgimg t-slds__bgimg-contain')
            video = div_object.find_all('iframe')

            image_links = [div['data-original'] for div in div_image]
            video_links = []

            for iframe in video:
                src = iframe['src']
                video_links.append(src)

            title = _soup.find('h1', class_='js-feed-post-title t-feed__post-popup__title t-title t-title_xxs')
            history_date = _soup.find('span', class_='js-feed-post-date t-feed__post-popup__date t-uptitle t-uptitle_sm')

            div_history_text = _soup.find('div', class_='t-redactor__tte-view')
            #his_list = []
            if div_history_text:
                history_text = div_history_text.find('div', class_='t-redactor__text')
                paragraphs = []
                for p in history_text.find_all_next(string=True):
                    stripped_p = p.strip()
                    if stripped_p:
                        paragraphs.append(stripped_p)
            else:
                paragraphs = []
            if paragraphs:
                paragraphs = paragraphs[:-14]
            data = {
                "title": str(title.get_text()),
                "history_date": str(history_date.get_text()),
                "images": image_links,
                "videos": video_links,
                "history_text": paragraphs
            }
            await asyncio.sleep(0.5)
            with open(f'webpages/{filename}.json', "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

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
