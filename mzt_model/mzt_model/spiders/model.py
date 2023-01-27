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
            print(x, at, au)
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
        driver_options.add_argument('--headless')  # 浏览器不提供可视化页面
        driver_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61"')  # 设置请求头的 User-Agent
        """ List of Chromium Command Line Switches
            https://peter.sh/experiments/chromium-command-line-switches/
        driver_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61"')  # 设置请求头的 User-Agent
        driver_options.add_argument('--window-size=200x100')  # 设置浏览器分辨率（窗口大小）
        driver_options.add_argument('--start-maximized')  # 最大化运行（全屏窗口），不设置，有时取元素会报错
        driver_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        driver_options.add_argument('--incognito')  # 隐身模式（无痕模式）
        driver_options.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
        driver_options.add_argument('--disable-javascript')  # 禁用 javascript
        driver_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片，提升速度
        driver_options.add_argument('--headless')  # 浏览器不提供可视化页面
        driver_options.add_argument('--ignore-certificate-errors')  # 禁用证书错误
        driver_options.add_argument('--disable-gpu')  # 禁用 GPU 加速
        driver_options.add_argument('--disable-software-rasterizer')  # 禁用 3D 软件光栅化器
        driver_options.add_argument('--disable-extensions')  # 禁用扩展
        """
        # 3. Initialize webdriver
        driver = webdriver.Edge(options=driver_options)
        # 4. Adjust window size and position
        driver.set_window_rect(x=440, y=500, width=1000, height=400)
        # 5. Selenium loads page (the url passed down from parse_album)
        driver.get(response.url)
        # 6. Selenium parses photos
        mp = int(response.css('#progressBar::attr(max)').extract_first())
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
