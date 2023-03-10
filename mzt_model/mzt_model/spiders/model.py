import scrapy
import re
from mzt_model.items import MztModelItem

import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep


class ModelSpider(scrapy.Spider):
    name = 'model'
    allowed_domains = []
    start_urls = ['https://mmzztt.com/photo/model/']
    # https://mmzztt.com/photo/model/
    # https://mmzztt.com/photo/model/yiming/
    # https://mmzztt.com/photo/4900
    # https://p.iimzt.com/2020/12/01c01a.jpg

    def parse(self, response, **kwargs):
        ml = response.xpath('/html/body/section/div/div/main/ul/li/div/div[2]/h2/a')
        x = 0
        for i in ml:
            x += 1
            mn = i.xpath('text()').extract_first()
            mu = i.xpath('@href').extract_first()
            print(x, mn, mu)
            yield response.follow(
                url=mu,
                callback=self.parse_album,
                meta={
                    'model_name': mn,
                },
            )

    def parse_album(self, response):
        mn = response.meta['model_name']
        al = response.xpath('/html/body/section/div/div/main/ul/li/div/div[3]/h2/a')
        x = 0
        for i in al:
            x += 1
            at = re.sub(
                pattern='([^\u4e00-\u9fff\u0041-\u005a\u0061-\u007a])',
                repl='',
                string=i.xpath('text()').extract_first()
            )
            au = i.xpath('@href').extract_first()
            print(x, mn, at, au)
            yield response.follow(
                url=au,
                callback=self.parse_photo,
                meta={
                    'model_name': mn,
                    'album_title': at,
                },
            )

    def parse_photo(self, response):
        mn = response.meta['model_name']
        at = response.meta['album_title']

        # 1. Reduce Selenium log level
        LOGGER.setLevel(logging.FATAL)
        # 2. Set webdriver options
        driver_options = Options()
        driver_options.add_argument('--headless')  # ?????????????????????????????????
        driver_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61"')  # ?????????????????? User-Agent
        """ List of Chromium Command Line Switches
            https://peter.sh/experiments/chromium-command-line-switches/
        driver_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61"')  # ?????????????????? User-Agent
        driver_options.add_argument('--window-size=200x100')  # ??????????????????????????????????????????
        driver_options.add_argument('--start-maximized')  # ????????????????????????????????????????????????????????????????????????
        driver_options.add_argument('--disable-infobars')  # ??????????????????????????????????????????????????????
        driver_options.add_argument('--incognito')  # ??????????????????????????????
        driver_options.add_argument('--hide-scrollbars')  # ??????????????????????????????????????????
        driver_options.add_argument('--disable-javascript')  # ?????? javascript
        driver_options.add_argument('--blink-settings=imagesEnabled=false')  # ??????????????????????????????
        driver_options.add_argument('--headless')  # ?????????????????????????????????
        driver_options.add_argument('--ignore-certificate-errors')  # ??????????????????
        driver_options.add_argument('--disable-gpu')  # ?????? GPU ??????
        driver_options.add_argument('--disable-software-rasterizer')  # ?????? 3D ??????????????????
        driver_options.add_argument('--disable-extensions')  # ????????????
        """
        # 3. Initialize webdriver
        driver = webdriver.Edge(options=driver_options)
        # 4. Adjust window size and position
        driver.set_window_rect(x=440, y=500, width=1000, height=400)
        # 5. Selenium loads page (the url passed down from parse_album)
        driver.get(response.url)
        # 6. Selenium parses photos
        mp = int(driver.find_element(by=By.ID, value='progressBar').get_property('max'))
        for x in range(0, min(15, mp)):
            print('//////// Photo: ', x+1, ' ////////')
            p = driver.find_element(
                by=By.CSS_SELECTOR,
                value='body > section:nth-child(3) > div > div > main > article > figure > img'
            )
            pu = p.get_attribute('src')
            # 7. Pass info to pipelines.py to download
            i = MztModelItem()
            i['model_name'] = mn
            i['album_title'] = at
            i['photo_url'] = pu
            yield i
            # 8. Selenium click next button
            np = driver.find_element(
                by=By.CSS_SELECTOR,
                value='.uk-position-center-right.f-swich'
            )
            np.click()
            sleep(1.2)
        # 9. Close
        driver.quit()
        print('//////// End of this album ////////')
