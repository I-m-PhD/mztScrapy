import scrapy
from mzt_top.items import MztTopItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time
from scrapy.http import HtmlResponse


class TopSpider(scrapy.Spider):
    name = 'top'
    allowed_domains = []
    start_urls = ['https://mmzztt.com/photo/top/']

    def parse(self, response, **kwargs):
        al = response.xpath('/html/body/section/div/div/main/ul/li/div/div[3]/h2/a')
        x = 0
        for i in al:
            x += 1
            ah = i.xpath('text()').extract_first()
            au = i.xpath('@href').extract_first()
            print(x, ah, au)
            yield response.follow(url=au, callback=self.parse_album, meta={'album_head': ah})

    @staticmethod
    def parse_album(response):
        ah = response.meta['album_head']
        mn = response.xpath('/html/body/section[1]/div/div/aside/div[1]/div[1]/div/div[2]/h3/a/text()').extract_first()
        # iu = response.xpath('/html/body/section[1]/div/div/main/article/figure/img/@src').extract_first()
        item = MztTopItem()
        item['model_name'] = mn
        item['album_head'] = ah
        # item['img_url'] = iu
        # print(item)
        # yield item
        """ Selenium """
        driver_options = Options()
        LOGGER.setLevel(logging.ERROR)
        driver_options.add_argument('--headless')
        driver_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61"')
        driver = webdriver.Chrome(options=driver_options)
        driver.set_window_rect(x=440, y=500, width=1000, height=400)
        driver.get(response.url)
        mxi = int(driver.find_element(by=By.ID, value='progressBar').get_property('max'))
        for x in range(0, min(15, mxi)):
            iu = driver.find_element(by=By.CSS_SELECTOR, value='body > section:nth-child(3) > div > div > main > article > figure > img').get_property('src')
            item['img_url'] = iu
            yield item
            driver.find_element(by=By.CSS_SELECTOR, value='.uk-position-center-right.f-swich').click()
            time.sleep(1)
            HtmlResponse(url=driver.current_url, body=driver.page_source, encoding='utf-8')
        driver.quit()
