#!/usr/bin/env python3
import requests
import re
import timeit
import json
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
from getconf import *
from atclibs import *
from selenium import webdriver

"""
NOTE:
billAddressType changes from 'different' to 'new' possibly depending on if shipping/bill address is the same
"""

base_url = 'http://www.footlocker.com'

# User input

email = ''
password = ''
use_early_link = True
early_link = 'http://www.footlocker.com/product/model:152915/sku:04775123/jordan-retro-7-mens/usa/white/blue/'
use_keyword = False
product_id = ''
size = '9.5'
size = footsites_parse_size(size)


def add_to_cart(url):
    response = session.get(url)
    soup = bs(response.text, 'html.parser')
    referer = response.url

    sku = soup.find('input', {'id': 'pdp_selectedSKU'})['value']
    model_num = soup.find('input', {'id': 'pdp_model'})['value']
    request_key = soup.find('input', {'id': 'requestKey'})['value']

    payload = {
        'BV_TrackingTag_QA_Display_Sort': '',
        'BV_TrackingTag_Review_Display_Sort': 'http://footlocker.ugc.bazaarvoice.com/8001/' + sku + '/reviews.djs?format=embeddedhtml',
        'coreMetricsCategory': 'blank',
        'fulfillmentType': 'SHIP_TO_HOME',
        'hasXYPromo': 'false',
        'inlineAddToCart': '0,1',
        'qty': '1',
        'rdo_deliveryMethod': 'shiptohome',
        'requestKey': request_key,
        'size': size,
        'sku': sku,
        'storeCostOfGoods': '0.00',
        'storeNumber': '00000',
        'the_model_nbr': model_num
    }
    headers = {
        'Accept': '*/*',
        'Origin': base_url,
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': referer,
        'Accept-Encoding': 'gzip, deflate',
    }

    session.post(base_url + '/catalog/miniAddToCart.cfm?secure=0&', headers=headers, data=payload)


def checkout():
    # login
    url = 'http://www.footlocker.com/login/login?secured=false&bv_RR_enabled=false&bv_AA_enabled=false&bv_JS_enabled=true&ignorebv=false&dontRunBV=true'
    driver.get(url)
    driver.switch_to.frame(driver.find_element_by_id('loginIFrame'))
    driver.find_element_by_id('login_email').send_keys(email)
    driver.find_element_by_id('login_password').send_keys(password)
    driver.find_element_by_tag_name('button').click()
    
    # checkout
    driver.get('http://www.footlocker.com/shoppingcart/default.cfm?sku=')
    


# Main
tick()

driver = webdriver.Chrome()
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/52.0.2743.116 Safari/537.36',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
})

url = ""

if use_early_link:
    url = early_link
else:
    url = base_url + '/product/sku:{}/'.format(product_id)

add_to_cart(url)
checkout()

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'en-US,en;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'',
    'Host':'shop.bdgastore.com',
    'If-None-Match':'',
    'Upgrade-Insecure-Requests': '1'
}
        
tock()
