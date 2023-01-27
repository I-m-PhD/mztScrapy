from scrapy import cmdline

cmdline.execute('scrapy crawl model -s LOG_FILE=all.log'.split())
