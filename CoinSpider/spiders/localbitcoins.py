# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from CoinSpider.items import LocalCoinsItem


class LocalbitcoinsSpider(scrapy.Spider):
    name = 'localbitcoins'
    allowed_domains = ['localbitcoins.com']
    start_urls = ['https://localbitcoins.com/buy-bitcoins-online/cny/.json']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url,
                dont_filter=True,
                callback=self.parse,)

    def parse(self, response):
        """
        get page count
        generate url
        """
        origin_data = json.loads(response.body)
        coin_data = origin_data['data'].get('ad_list')
        # get coins data
        for row in coin_data:
            url = row['actions'].get('public_view')
            row = row.get('data')
            user_info = row.get('profile')
            user = user_info.get('name')
            email = row.get('email')
            price = row.get('temp_price')
            price_currency = row.get('currency')
            require_min = row.get('min_amount')
            require_max = row.get('max_amount')
            trade_bank = row.get('bank_name')
            trade_method = row.get('online_provider')
            trade_msg = row.get('msg')
            trade_location = row.get('location_string')
            time = row.get('created_at')
            yield LocalCoinsItem(
                url=url,
                user=user,
                email=email,
                price=price,
                price_currency=price_currency,
                require_min=require_min,
                require_max=require_max,
                trade_bank=trade_bank,
                trade_location=trade_location,
                trade_method=trade_method,
                trade_msg=trade_msg,
                time=time,)
        # get pageinator data
        page_data = origin_data.get('pagination')
        if page_data.get('next'):
            yield Request(
                url=page_data.get('next'),
                callback=self.parse,
                method='GET',
                dont_filter=True)
