# -*- coding: utf-8 -*-
import json
import scrapy
import datetime
from urllib.parse import urlencode
from scrapy.http import Request
from scrapy.selector import Selector
from CoinSpider.items import CoinsItem


class CoincolaSpider(scrapy.Spider):
    name = 'coincola'
    allowed_domains = ['coincola.com']
    start_urls = ['https://www.coincola.com/buy']
    api_url = 'https://www.coincola.com/api/v1/contentslist/search'
    url_format = 'https://www.coincola.com/ad-detail/{}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    parent_format = {
        'country_code': 'CN',
        'limit': 1,
        'offset': 0,
        'sort_order': 'GENERAL',
        'type': 'SELL',
        'crypto_currency': 'BTC',
        '_csrf': '',
    }

    def start_requests(self):
        """
        get page data
        """
        # return request
        for url in self.start_urls:
            yield Request(
                url,
                dont_filter=True,
                callback=self.parse,)

    def parse(self, response):
        """
        get pages
        """
        # post format
        post_format = self.parent_format
        # get csrf
        select_obj = Selector(response=response)
        self.csrf = select_obj.css(
            'input[name="_csrf"]::attr("value")').extract_first()
        post_format['_csrf'] = self.csrf
        # get total rows
        yield Request(
            self.api_url,
            dont_filter=True,
            callback=self.pages,
            method='POST',
            headers=self.headers,
            body=urlencode(post_format))

    def pages(self, response):
        """
        get json
        """
        # get total count 
        origin_data = response.body.decode('utf-8')
        json_data = json.loads(origin_data)
        if not json_data.get('success'):
            return
        json_data = json_data.get('data')
        total = json_data.get('total')
        # generate data format
        post_format = self.parent_format
        post_format['_csrf'] = self.csrf
        post_format['limit'] = 10
        # use total count to get eacho json
        for count in range(0, total, 10):
            post_format['offset'] = count
            yield Request(
                self.api_url,
                dont_filter=True,
                callback=self.get_data,
                method='POST',
                headers=self.headers,
                body=urlencode(post_format)
            )
    
    def get_data(self, response):
        # get json data
        origin_data = response.body.decode('utf-8')
        json_data = json.loads(origin_data)
        if not json_data.get('success'):
            return
        json_data = json_data.get('data')
        json_data = json_data.get('advertisements')
        for sell_order in json_data:
            # generate user info
            user_info = sell_order.get('advertiser')
            user_trade_count = user_info.get('reputation')
            user_str_format = '{}({};{}%)'
            user_str_format = user_str_format.format(
                user_info.get('name'),
                user_trade_count.get('trade_count'),
                user_trade_count.get('feedback_score'),
            )
            # yield item object
            yield CoinsItem(
                url=self.url_format.format(sell_order.get('id')),
                price_currency=sell_order.get('currency'),
                require_min=sell_order.get('min_amount'),
                require_max=sell_order.get('max_amount'),
                trade_method=sell_order.get('payment_provider'),
                price=sell_order.get('price'),
                time=str(datetime.datetime.now())
            )
