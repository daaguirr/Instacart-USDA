import sys
import time
import traceback

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np

start = 0
products = pd.read_csv('usda/products.csv', sep=",")

blacklist = [6, 11, 20, 22, 40, 41, 44, 47, 54, 55, 56, 60, 73, 74, 75, 80, 82, 85, 87, 97, 101, 102, 109, 114, 118,
             126, 127, 132, 133]
white_products = products[~products['aisle_id'].isin(blacklist) & ~products['department_id'].isin([2, 11, 17])]
ans = []
size = len(white_products)
white_products = white_products.reset_index(drop=True)
white_products = white_products.copy()[start:]
white_products = white_products.reset_index(drop=True)


# white_products.to_csv('usda/whitelist.csv', encoding="utf-8", index=False)

def check_point(i_row):
    df = white_products.copy()[:+i_row]
    df.loc[:, 'ndbno'] = pd.Series(np.array(ans), index=df.index)
    df.to_csv(f"usda/checkpoints/checkpoint{start}_{start + i_row}.csv", encoding='utf-8', index=False)


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
browser = webdriver.Chrome(executable_path='PATH/chromedriver', chrome_options=option)

browser.get("https://ndb.nal.usda.gov/ndb/search/list")

cum_time = 0
for i, row in white_products.iterrows():
    t_start = time.time()
    try:
        q = row['product_name']
        text_area = browser.find_element_by_id('qlookup')
        text_area.clear()
        text_area.send_keys(q)

        button = browser.find_elements_by_xpath("//input[@value='Go']")[0]
        button.click()

        html = browser.page_source

        soup = BeautifulSoup(html, "lxml")
        try:
            tbody = soup.find("tbody")
            tr = tbody.find("tr")

            number = tr.find_all('td')[1].text.replace("\n", "").lstrip()
            ans += [number]
        except AttributeError:
            ans += ["-1"]

        if i % 1000 == 0 and i > 0:
            check_point(i + 1)
    except:
        check_point(i)
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
    time.sleep(1)
    t_end = time.time()
    cum_time += (t_end - t_start)
    print(
        f"Progress {(i+start)*100/size:.3f}% i = {i+start} "
        f"Estimated: {(len(white_products)-i) * cum_time/(i+1) :.0f} seg "
        f"last = {q}")
check_point(50000)
