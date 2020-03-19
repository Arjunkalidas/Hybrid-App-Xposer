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
from scrapy_splash   import SplashRequest


#from selenium import webdriver


class ApkturboSpider(scrapy.Spider):
    name = 'turboapks'
    allowed_domains = ['www.apkturbo.com']
    site_url = 'https://www.apkturbo.com';
    category_list = concaturl();
    start_url = 'https://www.apkturbo.com/app-search/'
    keyword = '' ;
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' ;
    headers = {'User-Agent': user_agent}
    flogger = logging.getLogger('apkturbo');
    flogger.setLevel(logging.DEBUG);
    log_file_name = 'scrapy.log';
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
             yield scrapy.Request(url=self.start_url+searchparam+'/page/1',callback=self.parse);

    def parse(self, response):

      print('list of response url'+str(response.url.split('/')[-1]));
      if response.url.split('/')[-1]!= self.pagecount:
        urlcomponents = response.url.split('/');
        print(urlcomponents);
        urlcomponents[-1] = str(int(urlcomponents[-1])+1);
        url = "/".join(urlcomponents);
        print(url);
        yield Request(
            url=url,
            callback=self.parse
          )

      aelements = response.xpath('//a[@class="app-list-app col-sm-6 col-md-4 col-xs-12 no-padding withripple"]/@href') \
          .getall();
      print(aelements);
      for url in aelements:
            print("URL Taken from page"+str(url));
            yield Request(
                url= url,
                headers=self.headers,
                callback=self.parse_section
            )
         # pdb.set_trace()



    def parse_section(self,response):

        urls = response.xpath('//a[@class="btn btn-raised btn-success btn-download gtm-track-click-download"]/@href').extract();
        for url in urls:
            self.logger.info('THE DOWNLOAD BUTTON URL %s',url)
            self.flogger.info('THE PACKAGE NAME OF APK DOWNLOADED %s',url.split("/")[5]);
            apk_name = url.split("/")[4]+str('.apk');
            print('APK NAME '+ apk_name);
            yield Request(
                url= url,
                headers=self.headers,
                callback=self.geturl
            )
    def geturl(self,response):
        urls = response.xpath('//p[@class="download-info-p"]/a/@href').getall();
        print("Item list"+str(len(urls)));
        for url in urls:
            final_url = self.site_url+url;
            print("Final Url"+final_url);
            yield Request(
                url=final_url,
                headers=self.headers,
                callback=self.save_apk
            )


    def save_apk(self,response):
            file_name ='' ;
            content_list = response.headers.getlist('Content-Disposition');
            for value in content_list:
                value = str(value);
                start_index = value.find('=');
                start_index +=2 ;
                end_index = value.find('-');
                end_index -= 1;
                file_name = value[start_index:end_index];
                file_name = re.sub('[^A-Za-z0-9]+','',file_name);
                file_name += str('.apk');
            self.logger.info('THE FINAL FILE NAME %s',file_name);
            path = os.path.join('APK_DIR',file_name);
            home = expanduser("~");
            path = os.path.join(home,path);
            self.logger.info('THE FINAL PATH %s', os.path.dirname(path));
            if not os.path.exists(os.path.dirname(path)):
                self.logger.info('In not dir');
                os.makedirs(os.path.dirname(path));
            os.chdir(os.path.dirname(path))
            self.logger.info('Saving APK %s', path)
            with open(path, 'wb') as f:
                f.write(response.body)
