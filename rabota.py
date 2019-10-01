import codecs

import requests
from bs4 import BeautifulSoup as BS
import time

session = requests.Session()
headers = {'User-Agent': 'Mozilla/0.5 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'

domain = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'
jobs = []
urls = []
urls.append(url)
urls.append(domain+'/pg2')


for url1 in urls:
    time.sleep(2)
    req = session.get(url1, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, 'html.parser')
        div_list = bsObj.find_all('article', attrs={'class':'f-vacancylist-vacancyblock'})
        for div in div_list:
            title = div.find('h3', attrs={'class':'fd-beefy-gunso'}).text
            href = div.a['href']
            short = div.find('p', attrs={'class':'f-vacancylist-shortdescr'}).text
            company = div.p.text
            jobs.append({'href': href,
                         'title': title,
                         'descr': short,
                         'company': company})


#data = bsObj.prettify()#.encode('utf8')
template = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head><body>'
end = '</body></html>'
content = '<h2> Rabota.ua</h2>'
for job in jobs:
    content += '<a href= "{href}" target="_blank">{title}</a><br/><p>{descr}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br/><br/>'
data = template + content + end
handle = codecs.open('work_ua.html', 'w', 'utf-8')
handle.write(str(data))
handle.close()