from scrapy import cmdline

cmdline.execute('scrapy crawl top -s LOG_FILE=all.log'.split())
