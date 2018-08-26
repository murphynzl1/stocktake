
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
from urllib2 import HTTPError

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open('http://m.merquip.co.nz/User/Login')


# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=0)

# User credentials
br.form['LoginId'] = 'nigel'
br.form['Password'] = 'Nigel9272'

# Login
br.submit()

h = html2text.HTML2Text()
# Ignore converting links from HTML
h.ignore_links = True

#Get Items from CSV file
with open("items.csv",'r') as f:
    for i in f:
        i=i.strip('\n')
        b=i.split(",")

        #goto stock item
        no=b[0]
        desc=b[1]

        try:
            page=h.handle(br.open('http://m.merquip.co.nz/Stock/Details/'+str(no)).read())
        except HTTPError, e:
            continue
        except UnicodeDecodeError, d:
            #split page by end of line to find stock on hand.
            content=page.split("\n")

            for i in content:
                if "Nigel" in i:
                    stock=i.split("|")
                    break

            if "-" not in stock[5]:
                print(str(no)+","+desc+","+str(stock[5])+"\n")#print items greater than 0

        #split page by end of line to find my stock on hand.
        content=page.split("\n")

        for i in content:
            if "Nigel" in i:
                stock=i.split("|")
                break

        if "-" not in stock[5]:
            print(str(no)+","+desc+","+str(stock[5])+"\n")#print items greater than 0
