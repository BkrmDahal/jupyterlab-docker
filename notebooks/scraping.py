#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 22:10:21 2018

@author: Bikram 
"""

## install chrome 
# apt-get install libxss1 libappindicator1 libindicator7 wget
# apt-get install -f
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# dpkg -i google-chrome*.deb

## download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
# wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
# unzip chromedriver_linux64.zip
# mv chromedriver /usr/local/bin/


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import defaultdict
from tqdm import tqdm
import glob

import pandas as pd
import csv

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--user-data-dir=/root/.config/google-chrome/Default")

# details of ca
details = []
total_pages = 37
base_url = "https://www.caknowledgeclub.com/caauditfirms/Chartered_Accountants/{}"
city_details = {'city':[ 'chennai/tamilnadu', 'mumbai/maharashtra'],
          'pages':[13, 37]}
# city_details = {'city':[ 'bangalore/karnataka', 'chennai/tamilnadu', 'mumbai/maharashtra'],
#           'pages':[13, 13, 37]}
url_filename = 'url_{}.csv'
detail_filename = 'detail_{}.csv'

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
chrome_driver = '/usr/local/bin/chromedriver'

# make selenium drivers
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

# get the link to page
def get_more_link_url(city, pages):
    url = base_url.format(city)
    driver.get(url)
    url_file = url_filename.format(city.split('/')[0])
    
    for page in tqdm(range(1, pages+1)):
        # go to next page
        try:
            goto = driver.find_element_by_class_name('goto')
            goto.clear()
            goto.send_keys(page)
            goto = driver.find_element_by_class_name('go_button')
            goto.click()
            time.sleep(5)
        except Exception as e:
            print("    skipped ", page, "reason: ", e)
            time.sleep(5)
        
        
        soup = driver.page_source
        soup = BeautifulSoup(soup, "lxml")
        lists = soup.find_all(attrs={'class':'more-link'})
        urls = [l.find_all('a')[0].get('href') for l in lists ]
        
        # save  the page
        try:
            with open(url_file, 'a') as f:
                writer = csv.writer(f);
                writer.writerows(zip(urls))
        except:
            with open(url_file, 'w') as f:
                writer = csv.writer(f);
                writer.writerows(zip(urls))
    
    # read file and write back the unique url
    with open(url_file) as csvfile:
        readCSV = csv.reader(csvfile)
        urls = [row[0] for row in readCSV]
    urls = list(set(urls))

    # write unique lists
    with open(url_file,'w') as f:
        writer = csv.writer(f);
        writer.writerows(zip(urls))

# get url files name
url_files = glob.glob("url*.csv")

# get details for each url
url_files = ['url_delhi.csv']
for f in url_files:
    detail_file = f.replace('url', 'detail')
    
    # read urls as list
    with open(f) as csvfile:
        readCSV = csv.reader(csvfile)
        urls = [row[0] for row in readCSV]

    # scraped each list
    for url in tqdm(urls[10:90]):
        try:
            driver.get(url)
            soup = driver.page_source
            soup = BeautifulSoup(soup, "lxml")

            # get the profile
            profiles = soup.find_all(attrs={'class':'profileaddress'})

            # get the details from page
            for profile in profiles:
                detail = []
                for line in profile:
                    if line != '\n':
                        try:
                            data = line.find('a')
                            data = data['href']
                        except:
                            data = line.get_text().strip()

                        if 'mailto' in data:
                            data = data[7:]
                        detail.append(data)
                detail.append(url)


            # append data to list
            if os.path.isfile(detail_file):
                try:
                    with open(detail_file,'a') as f:
                        writer = csv.writer(f);
                        writer.writerow(detail)
                except:
                    driver.close()
                    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
                    
                    print("skipped ", url)
            else:
                try:
                    with open(detail_file,'w') as f:
                        writer = csv.writer(f);
                        writer.writerow(detail)
                except:
                    driver.close()
                    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
                    print("skipped ", url)

        except Exception as e:
            driver.close()
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
            print(url, ">>>>", e)
            
# combine data
import glob
import pandas as pd

files = glob.glob("detail*.csv")

files

df = pd.DataFrame()
for i in files:
    temp = pd.read_csv(i)
    temp['city'] = i.split('_')[-1].split('.')[0]
    df = df.append(temp)

df = df.drop_duplicates()

df.shape

df.to_csv('master_CA_4_city.csv')
