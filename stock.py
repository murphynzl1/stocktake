
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text

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

page=h.handle(br.open('http://m.merquip.co.nz/Stock/Details/853009').read())
content=page.split("\n")
a=0
no=853009

for i in content:
    if "Nigel" in i:
        stock=content[a].split("|")
        value={no:stock[5]}
        print[float(value[no])]
    a+=1
