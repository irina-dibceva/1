import datetime
import time
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render
from scraping.models import *
from scraping.forms import FindVacancy
from scraping.utils import *


def home(request):
    return render(request, 'base.html')


def list_today(request):
    today = datetime.date.today()
    city = City.objects.get(name='Kiev')
    speciality = Specialty.objects.get(name='Python')
    qs = Vacancy.objects.filter(city=city.id, speciality=speciality.id, timestamp=today)
    if qs:
        return render(request, 'scraping/list.html', {'jobs': qs})
    return render(request, 'scraping/list.html')


def list_vacancy(request):
    today = datetime.date.today()
    form = FindVacancy
    if request.GET:
        try:
            city_id = int(request.GET.get('city'))
            speciality_id = int(request.GET.get('speciality'))
        except ValueError:
            raise Http404('Page not found')
        context = {'form': form}
        qs = Vacancy.objects.filter(city=city_id, speciality=speciality_id, timestamp=today)
        if qs:
            context['jobs'] = qs
            return render(request, 'scraping/list.html', context)
    return render(request, 'scraping/list.html', {'form': form})


def home_list(request):
    city = City.objects.get(name='Kiev')
    speciality = Specialty.objects.get(name='Python')
    url_qs = Url.objects.filter(city=city, speciality=speciality)
    site = Site.objects.all()
    url_w = url_qs.get(site=site.get(name='Work.ua')).url_address
    url_r = url_qs.get(site=site.get(name='Rabota.ua')).url_address
    url_dj = url_qs.get(site=site.get(name='Djinni.co')).url_address
    url_d = url_qs.get(site=site.get(name='Dou.ua')).url_address
    jobs = []
    jobs.extend(djinni(url_dj))
    jobs.extend(dou(url_d))
    jobs.extend(rabota(url_r))
    jobs.extend(work(url_w))
    v = Vacancy.objects.filter(city=city.id, speciality=speciality.id).values('description')
    description_list = [i['description'] for i in v]
    for job in jobs:
        if job['descr'] not in description_list:
            vacancy = Vacancy(city=city, speciality=speciality, url_vacancy=job['href'],
                              title=job['title'], description=job['descr'],
                              company=job['company'])
            try:
                vacancy.save()
            except IntegrityError:
                'This vacancy is exist'

    return render(request, 'scraping/list.html', {'jobs': jobs})
