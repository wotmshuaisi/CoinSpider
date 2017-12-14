#! /bin/sh
export PATH=$PATH:/usr/local/bin
cd /home/CoinSpider/
python3 cleardatabase.py
nohup scrapy crawl localbitcoins >> localbitcoins.log 2>&1 &
nohup scrapy crawl coincola >> coincola.log 2>&1 &
