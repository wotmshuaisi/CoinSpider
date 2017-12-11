# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from CoinSpider.items import LocalCoinsItem


class LocalbitcoinsSpider(scrapy.Spider):
    name = 'localbitcoins'
    allowed_domains = ['localbitcoins.com']
    start_urls = ['https://localbitcoins.com/buy-bitcoins-online/cny/.json']
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'upgrade-insecure-requests': 1,
        'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'cookie': '__cfduid=da6b104b729c8864d1600e2694661522d1511629878; lbc_browser_id=DTQDXRNHMETMEIKTWXPPGRAQVSLIDMWE; empty_visit_id=1; __lc.visitor_id.5492471=S1511629917.9c843a142c; countrycode=CN; lon=120.1614; lat=30.2936; django_language=en; location_string="Hangzhou\054 China"; mp_mixpanel__c=33; cf_clearance=ffb78be571e90f50d4fbc0bd445f99efbdb3b51c-1512878996-900; csrftoken=GZwOwFHzuaOigtCucIWYkHkmmsGVxVa0; localbitcoinssession=None; mp_e9b0d9a5818a56e8691a792577467dfd_mixpanel=%7B%22distinct_id%22%3A%20%2215ff429a30f533-04be7de8303f8b-1f2a1709-100200-15ff429a3104b3%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Flocalbitcoins.com%2Fcountry%2FCN%22%2C%22%24initial_referring_domain%22%3A%20%22localbitcoins.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22gclid%22%3A%20%22Cj0KCQiAsK7RBRDzARIsAM2pTZ-h9pKfsnSrSrlPP9_MIWdMcnpuPfKnAqEWyLEG30i-LlQfXB15gWIaAobWEALw_wcB%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%2C%22ch%22%3A%20%223yyg%22%2C%22gclid%22%3A%20%22Cj0KCQiAsK7RBRDzARIsAM2pTZ-h9pKfsnSrSrlPP9_MIWdMcnpuPfKnAqEWyLEG30i-LlQfXB15gWIaAobWEALw_wcB%22%2C%22%24search_engine%22%3A%20%22google%22%7D; __utma=14050346.1183651974.1511629887.1512874167.1512878999.4; __utmb=14050346.4.10.1512878999; __utmc=14050346; __utmz=14050346.1512871234.2.2.utmgclid=Cj0KCQiAsK7RBRDzARIsAM2pTZ-h9pKfsnSrSrlPP9_MIWdMcnpuPfKnAqEWyLEG30i-LlQfXB15gWIaAobWEALw_wcB|utmccn=(not%20set)|utmcmd=(not%20set)|utmctr=(not%20provided); _gac_UA-32479826-1=1.1512871234.Cj0KCQiAsK7RBRDzARIsAM2pTZ-h9pKfsnSrSrlPP9_MIWdMcnpuPfKnAqEWyLEG30i-LlQfXB15gWIaAobWEALw_wcB'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url,
                dont_filter=True,
                callback=self.parse,
                headers=self.headers)

    def parse(self, response):
        """
        get page count
        generate url
        """
        origin_data = json.loads(response.body)
        coin_data = origin_data['data'].get('ad_list')
        # get coins data
        for row in coin_data:
            user_info = row.get('profile')
            url = row.get('public_view')
            user = user_info.get('name')
            email = row.get('email')
            price = row.get('temp_price')
            price_currency = row.get('currency')
            require_min = row.get('min_amount')
            require_max = row.get('max_amount')
            trade_bank = row.get('bank_name')
            trade_method = row.get('created_at')
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
                headers=self.headers,
                dont_filter=True)
