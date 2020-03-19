# -*- coding: utf-8 -*-
# Author: himanshu Chourasia
import logging
import scrapy
import re
import os.path
from os.path import expanduser
import pdb
from scrapy.http import Request
from Utility import concaturl
# import items
import json
from scrapy_splash import SplashRequest


#from selenium import webdriver


class ApkmonkSpider(scrapy.Spider):
    name = 'monkapks'
    allowed_domains = ['www.apkmonk.com','apk.apkmonk.com']
    site_url = 'https://www.apkmonk.com';
    category_list = concaturl();
    start_url = 'https://www.apkmonk.com'
    keyword = '' ;
    download_delay = 1
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' ;
    headers = {'User-Agent': user_agent}
    flogger = logging.getLogger('apkturbo');
    flogger.setLevel(logging.DEBUG);
    log_file_name = 'scrapy_apkmonk.log';
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # create file handler which logs even debug messages
    f_path = os.path.join('SCRAPY_LOG_DIR',log_file_name );
    f_home = expanduser("~");
    f_path = os.path.join(f_home, f_path);
    print('THE FINAL FILE LOGGING PART %s',os.path.dirname(f_path))
    if not os.path.exists(os.path.dirname(f_path)):
        print('Directory Not found creating a directory for log file')
        os.makedirs(os.path.dirname(f_path));
    os.chdir(os.path.dirname(f_path))
    fh = logging.FileHandler(f_path);
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG);
    flogger.addHandler(fh);
    def start_requests(self):
        for searchparam in self.category_list:
             self.keyword = searchparam;
             yield scrapy.Request(url=self.start_url+'/search?q='+searchparam,callback=self.parse);

    def parse(self, response):



      aelements = response.xpath('//div[@class="col l7 s7 offset-l1 offset-s1 m7 offset-m1"]//a/@href') \
          .getall();
      print(aelements);
      for url in aelements:
            print("URL Taken from page"+str(url));
            yield Request(
                url= self.start_url+url,
                headers=self.headers,
                callback=self.parse_section
            )
         # pdb.set_trace()



    def parse_section(self,response):

        urls = response.xpath('//a[@id="download_button"]/@href').extract();
        for url in urls:
            if 'download-app' in url:
                # print(url)
                pkg_key = url.split('/')
                self.logger.info('THE DOWNLOAD BUTTON URL %s', url)
                self.flogger.info('THE PACKAGE NAME OF APK DOWNLOADED %s',pkg_key[4]);
                yield Request(
                    url=f'https://www.apkmonk.com/down_file?pkg={pkg_key[4]}&key={pkg_key[5]}',
                    callback=self.get_url
                )

    def get_url(self, response):
        response_json = json.loads(response.body_as_unicode())
        if response_json['resp'] == 'success':
            yield Request(
                url=response_json['url'],
                callback=self.save_pdf
                )

    def save_pdf(self, response):
        # pdb.set_trace()
        file_name = response.url.split("/")[-1].split("?")[0] ;
        path = os.path.join('APK_DIR', file_name);
        home = expanduser("~");
        path = os.path.join(home, path);
        self.logger.info('THE FINAL PATH %s', os.path.dirname(path));
        if not os.path.exists(os.path.dirname(path)):
            self.logger.info('In not dir');
            os.makedirs(os.path.dirname(path));
        os.chdir(os.path.dirname(path))
        self.logger.info('Saving APK %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
