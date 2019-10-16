# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import time


class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome(service_args=service_args)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):

        page = request.meta.get('page')
        self.logger.debug(request.url)

        if page:
            try:
                self.browser.get(request.url)
                print(request.url)
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ybq-page-header > ui-view > div:nth-child(2) > div > div.product-section.layout-wrap.layout-row > div:nth-child(1)')))
                time.sleep(1)
                js = "var q=document.documentElement.scrollTop=10000"
                self.browser.execute_script(js)
                time.sleep(1)
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                    status=200)
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)
        else:
            try:
                self.browser.get(request.url)
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-dig-img')))
                time.sleep(1)
                js = "var q=document.documentElement.scrollTop=10000"
                self.browser.execute_script(js)
                time.sleep(1)
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                    status=200)
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))