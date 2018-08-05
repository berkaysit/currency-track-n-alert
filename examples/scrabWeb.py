from bs4 import BeautifulSoup
import requests
from time import gmtime, strftime
import time
import datetime
import random
import sys
import dovIncMail

url = "https://www.ziraatbank.com.tr/tr/fiyatlar-ve-oranlar"

r  = requests.get(url)
page = r.text
soup = BeautifulSoup(page, "html.parser")
# div = soup.find("div", id="result-dovizkur")

##    UsdAlis = float(div.text[4:13].replace(',','.'))
##    UsdSatis = float(div.text[16:25].replace(',','.'))

##print(soup.prettify())
print("------------------------------")
##print(div)
table = soup.find_all('table')[8] #.get_text()

table_body = table.find('tbody')

#print(table)
print(table_body)

rows = table_body.find_all('tr')
for row in rows:
    #cols = row.find_all('td')

    if row.find_all('td')[0].get_text() == 'USD':
        UsdAlis = row.find_all('td')[2].get_text()
        UsdSatis = row.find_all('td')[3].get_text()
        print("Buldum: " + str(UsdAlis.replace(',','.')) )
        print("Buldum: " + str(UsdSatis.replace(',','.')) )
    
##    cols = [ele.text.strip() for ele in cols]
##    data.append([ele for ele in cols if ele]) # Get rid of empty values
