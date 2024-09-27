#Code to collect security practices of each app

import pandas as pd
import re
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

def preprocess(blocks,df):
    if len(blocks) > 0:
        # 1. No data shared preprocessing
        sub_block = blocks[0].find_element(By.CLASS_NAME,'XgPdwe')
        div_elements = sub_block.find_elements(By.XPATH, './*[self::div]')
        part1 = {}
        
        for div in div_elements:
            sub_part = {}           
            key = div.find_element(By.CLASS_NAME,'aFEzEb').text
            div_value = div.find_element(By.CLASS_NAME,'GcNQi')           
            h4_elem_part1 = div_value.find_elements(By.CSS_SELECTOR, 'h4.pcmFvf')
            div_elem_part1 = div_value.find_elements(By.CSS_SELECTOR, 'div.FnWDne')
            for h4, div in zip(h4_elem_part1, div_elem_part1):               
                sub_key = h4.find_element(By.CLASS_NAME,'qcuwR').text                
                sub_value = div.text
                sub_part[sub_key] = sub_value
            part1[key]=sub_part
           
        shared.append(part1)

        # 2. Data Collected Preprocessing
        sub_block = blocks[1].find_element(By.CLASS_NAME,'XgPdwe')
        div_elements = sub_block.find_elements(By.XPATH, './*[self::div]')
        part2 = {}
        
        for div in div_elements:
            sub_part = {}           
            key = div.find_element(By.CLASS_NAME,'aFEzEb').text
            div_value = div.find_element(By.CLASS_NAME,'GcNQi')           
            h4_elem_part2 = div_value.find_elements(By.CSS_SELECTOR, 'h4.pcmFvf')
            div_elem_part2 = div_value.find_elements(By.CSS_SELECTOR, 'div.FnWDne')
            for h4, div in zip(h4_elem_part2, div_elem_part2):               
                sub_key = h4.find_element(By.CLASS_NAME,'qcuwR').text                
                sub_value = div.text
                sub_part[sub_key] = sub_value
            part2[key]=sub_part
           
        collected.append(part2)

        # 3. Security Practices
        if len(blocks) == 3:
            sub_block = blocks[2].find_element(By.CLASS_NAME,'XgPdwe')
            div_elements = sub_block.find_elements(By.XPATH, './*[self::div]')
            part3 = {}
            for elem in div_elements:
                h3_elem_part3 = elem.find_element(By.CLASS_NAME, 'aFEzEb').text
                div_elem_part3 = elem.find_element(By.CLASS_NAME, 'fozKzd').text
                part3[h3_elem_part3]=div_elem_part3
                       
        else:
            part3 = "No Information on security"
            
        security.append(part3)
    else:
        info = "No Information"
        shared.append(info)
        collected.append(info)
        security.append(info)

    return shared, collected, security


if __name__ == '__main__':
    df = pd.read_csv('dataset/meta_app.csv')
    k = df['app_package'].unique()
    length = len(k)
    print(length)
    shared=[]
    collected=[]
    security=[]
    count = 0
    for ele in k:
        print(count, str(ele))
        count = count + 1
        url = "https://play.google.com/store/apps/datasafety?id=" + str(ele)
        driver.get(url)
        try:
            more_icon = driver.find_elements(By.XPATH, './/i[@class="google-material-icons VfPpkd-kBDsod tGvJLc"]')
            for ele in more_icon:
                ele.click()
        except:
            pass
        
        try:
            blocks = driver.find_elements(By.XPATH, './/div[@class="Mf2Txd"]')
            preprocess(blocks,df)
            
        except:
            pass
    df["Data Shared"] = shared
    df["Data Collected"] = collected
    df["Security Practices"] = security
    
    #Save it in CSV file
    df.to_csv('dataset/google_playstore_datasafety.csv')
