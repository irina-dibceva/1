import codecs

import requests
from bs4 import BeautifulSoup as BS
import time

session = requests.Session()
headers = {'User-Agent': 'Mozilla/0.5 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
url = 'https://djinni.co/jobs/?primary_keyword=Python&location=%D0%9A%D0%B8%D0%B5%D0%B2'

domain = 'https://djinni.co/jobs/?primary_keyword=Python&location=%D0%9A%D0%B8%D0%B5%D0%B2'
#&page=2
jobs = []
urls = []
urls.append(url)
urls.append(domain+'&page=2')

for url1 in urls:
    time.sleep(2)
    req = session.get(url1, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, 'html.parser')
        div_list = bsObj.find_all('li', attrs={'class':'list-jobs__item'})
        for div in div_list:
            titl = div.find('div', attrs={'class':'list-jobs__title'})
            title = titl.text
            href = titl.a['href']
            sh = div.find('div', attrs={'class':'list-jobs__description'})
            short = sh.p.text
            company = 'No name'
            jobs.append({'href':  href,
                         'title': title,
                         'descr': short,
                         'company': company
                         })
        print(href,
              title,
              short,
              )

#data = bsObj.prettify()#.encode('utf8')
template = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head><body>'
end = '</body></html>'
content = '<h2> Work.ua</h2>'
for job in jobs:
    content += '<a href= "{href}" target="_blank">{title}</a><br/><p>{descr}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br/><br/>'
data = template + content + end
handle = codecs.open('work_ua.html', 'w', 'utf-8')
handle.write(str(data))
handle.close()