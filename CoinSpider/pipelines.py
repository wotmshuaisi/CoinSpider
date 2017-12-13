# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from influxdb import InfluxDBClient
from CoinSpider import settings
from scrapy.exceptions import DropItem
import logging
import traceback

_logging = logging.getLogger('CoinSpider.pipelines')


class CoinspiderInfluxdb(object):
    parent_tpl = {
        "measurement": settings.INFLUX_TABLE,
        "tags": {
        },
        "time": '',
        "fields": {
        }
    }

    def _check_repeat(self, url):
        return bool(self.client.query(
            "select * from localbitcoins where url='%s'" % url))

    def open_spider(self, spider):
        _logging.info('create influxdb connections...')
        try:
            self.client = InfluxDBClient(
                host=settings.INFLUX_HOST,
                port=settings.INFLUX_PORT,
                username=settings.INFLUX_USER,
                password=settings.INFLUX_PASS,
                database=settings.INFLUX_DATABASE
            )
            self.client.query('drop measurement %s;' % settings.INFLUX_TABLE)
        except Exception as e:
            _logging.error('connection error: %s', traceback.format_exc())

    def process_item(self, item, spider):
        data_tpl = self.parent_tpl
        data_tpl['tags'] = {
            'index_price': item['price'],
            'index_url': item['url'],
        }
        if item.get('time'):
            data_tpl['time'] = item['time']
        data_tpl['fields'] = {
            'price': item['price'],
            'price_currency': item.get('price_currency'),
            'trade_bank': item.get('trade_bank'),
            'trade_method': item.get('trade_method'),
            'trade_location': item.get('trade_location'),
            'user': item.get('user'),
            'email': item.get('email'),
            'url': item.get('url'),
            'trade_msg': item.get('trade_msg'),
            'require_min': item.get('require_min'),
            'require_max': item.get('require_max')
        }
        self.client.write_points([data_tpl])
        raise DropItem
    
    def close_spider(self, spider):
        logging.info('close influxdb connections...')
        self.client.close()
