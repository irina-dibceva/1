import codecs

import requests
from bs4 import BeautifulSoup as BS
import time

session = requests.Session()
headers = {'User-Agent': 'Mozilla/0.5 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'

domain = 'https://www.work.ua'
jobs = []
urls = []
urls.append(url)
req = session.get(url, headers=headers)
if req.status_code == 200:
    bsObj = BS(req.content, 'html.parser')
    pagination = bsObj.find('ul', attrs={'class': 'pagination'})
    if pagination:
        pages = pagination.find_all('li', attrs={'class': False})
        for page in pages:
            urls.append(domain + page.a['href'])


for url1 in urls:
    time.sleep(2)
    req = session.get(url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, 'html.parser')
        div_list = bsObj.find_all('div', attrs={'class':'vacancy'})
        for div in div_list:
            titl = div.find('div', attrs={'class':'title'})
            title = titl.a.text
            href = titl.a['href']
            company = div.find('a', attrs={'class':'company'}).text
            short = div.find('div', attrs={'class':'sh-info'}).text
            jobs.append({'href': href,
                         'title': title,
                         'descr': short,
                         'company': company})
        print(href,
              title,
              short,
              company)

#data = bsObj.prettify()#.encode('utf8')
template = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head><body>'
end = '</body></html>'
content = '<h2> Dou.ua</h2>'
for job in jobs:
    content += '<a href= "{href}" target="_blank">{title}</a><br/><p>{descr}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br/><br/>'
data = template + content + end
handle = codecs.open('work_ua.html', 'w', 'utf-8')
handle.write(str(data))
handle.close()