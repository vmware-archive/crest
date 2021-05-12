# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT
import logging
import traceback
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def to_valid_url(url):
    if 'http' not in url:
        if 'www.' not in url:
            url = 'www.'+url
        url = 'http://'+url
    return url 

def remove_category_add_param(output):
    categories_without_zero_count ={}
    total_count = 0
    for category in output["categories"].keys():
        count = output["categories"][category]["count"]
        if count!=0:
            categories_without_zero_count[category] = output["categories"][category]
            total_count += count
    output["categories"] = categories_without_zero_count
    output["statistics"]["allitemcount"] = total_count
    return output

def get_driver():
    logging.debug("Inside get_driver function")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
    # chrome_options.add_argument('Upgrade-Insecure-Requests=1')
    # chrome_options.add_argument('DNT=1')
    # chrome_options.add_argument('accept=*/*')
    # chrome_options.add_argument('Accept-Language= en-US,en;q=0.5')
    # chrome_options.add_argument('Accept-Encoding=gzip, deflate')
    prefs = {
        "profile.default_content_setting_values": {
            "cookies": 2,
            "plugins": 2,
            "popups": 2,
            "notifications": 2,
            "push_messaging": 2,
        }
    }
    # capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    # capabilities['acceptSslCerts'] = True 
    # capabilities['acceptInsecureCerts'] = True

    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options
    )
    # driver = webdriver.Chrome(options=chrome_options
    return driver

def check_url():
    try:
        response = requests.get(self.url)
        logging.debug("URL is valid and exists on the internet")
        return True
    except requests.ConnectionError as exception:
        logging.error("URL does not exist on Internet")
        return False