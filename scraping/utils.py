import codecs

import requests
from bs4 import BeautifulSoup as BS
import time

headers = {'User-Agent': 'Mozilla/0.5 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def djinni(url):
    session = requests.Session()
    domain = 'https://djinni.co/jobs/?primary_keyword=Python&location=%D0%9A%D0%B8%D0%B5%D0%B2'

    jobs = []
    urls = [url, domain + '&page=2']

    for url1 in urls:
        time.sleep(2)
        req = session.get(url1, headers=headers)
        if req.status_code == 200:
            bsObj = BS(req.content, 'html.parser')
            div_list = bsObj.find_all('li', attrs={'class': 'list-jobs__item'})
            for div in div_list:
                titl = div.find('div', attrs={'class': 'list-jobs__title'})
                title = titl.text
                href = 'https://djinni.co'+titl.a['href']
                sh = div.find('div', attrs={'class': 'list-jobs__description'})
                short = sh.p.text
                company = 'No name'
                jobs.append({'href': href,
                             'title': title,
                             'descr': short,
                             'company': company
                             })
    return jobs


def dou(url):
    session = requests.Session()
    jobs = []
    urls = [url]

    for url1 in urls:
        time.sleep(2)
        req = session.get(url1, headers=headers)
        if req.status_code == 200:
            bsObj = BS(req.content, 'html.parser')
            div_list = bsObj.find_all('div', attrs={'class': 'vacancy'})
            for div in div_list:
                titl = div.find('div', attrs={'class': 'title'})
                title = titl.a.text
                href = titl.a['href']
                company = div.find('a', attrs={'class': 'company'}).text
                short = div.find('div', attrs={'class': 'sh-info'}).text
                jobs.append({'href': href,
                             'title': title,
                             'descr': short,
                             'company': company})
    return jobs


def rabota(url):
    session = requests.Session()
    domain = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'
    jobs = []
    urls = [url, domain + '/pg2']

    for url1 in urls:
        time.sleep(2)
        req = session.get(url1, headers=headers)
        if req.status_code == 200:
            bsObj = BS(req.content, 'html.parser')
            div_list = bsObj.find_all('article', attrs={'class': 'f-vacancylist-vacancyblock'})
            for div in div_list:
                title = div.find('h3', attrs={'class': 'fd-beefy-gunso'}).text
                href = 'https://rabota.ua'+div.a['href']
                short = div.find('p', attrs={'class': 'f-vacancylist-shortdescr'}).text
                company = div.p.text
                jobs.append({'href': href,
                             'title': title,
                             'descr': short,
                             'company': company})
    return jobs


def work(url):
    session = requests.Session()
    domain = 'https://www.work.ua'
    jobs = []
    urls = [url]
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
        req = session.get(url1, headers=headers)
        if req.status_code == 200:
            bsObj = BS(req.content, 'html.parser')
            div_list = bsObj.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                titl = div.find('h2')
                title = titl.a['title']
                href = 'https://www.work.ua'+titl.a['href']
                short = div.p.text
                company = div.b.text
                jobs.append({'href': href,
                             'title': title,
                             'descr': short,
                             'company': company})
    return jobs
