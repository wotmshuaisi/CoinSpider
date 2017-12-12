#! /bin/sh
export PATH=$PATH:/usr/local/bin
cd /home/CoinSpider/
nohup scrapy crawl localbitcoins >> localbitcoins.log 2>&1 &
