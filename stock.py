from bs4 import BeautifulSoup as bs
import requests
import re
import time  # delay requests
import os


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


URL = 'https://m.merquip.co.nz/'
LOGIN_ROUTE = 'User/Login'
onhand = []  # stock onhand
w = 0  # used to count requests
username = input('Please enter username: ') #username
password = input('Please enter password: ' ) #password

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'origin': URL, 'referer': URL + LOGIN_ROUTE}

s = requests.session()

login_payload = {
    'LoginId': username,
    'Password': password,
}

login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)

cookies = login_req.cookies

with open("items.csv", 'r') as f:
    for i in f:
        i = i.strip('\n')
        b = i.split(",")
        no = b[0]  # stock number
        desc = b[1]
        stock = []
        c = 'n'  # Y when my stock value is found
        w += 1  # every 50 requests wait 2sec

        # check if stock exists in TTM
        check = s.get(URL + '/Stock/Details/' + str(no))
        if check.status_code == 404:
            onhand.append(str(no) + "," + desc + " , not in TTM \n")
            continue

        soup = bs(s.get(URL + '/Stock/Details/' + str(no)).text, 'html.parser')
        tbody = soup.find_all('td')

        for content in tbody:
            content = remove_html_tags(str(content))

            if content.find("Nigel") > -1 or c == 'y':
                c = 'y'
                stock.append(content)
        onhand.append(str(no) + "," + desc + " , " + str(stock[5]) + "\n")
        print(no)
        if w == 50:
            time.sleep(2)
            w = 0

# write stocktake to filw
if os.path.exists("onhand.csv"):
    os.remove("onhand.csv")

file1 = open("onhand.csv", "w")
file1.writelines(onhand)
file1.close()
