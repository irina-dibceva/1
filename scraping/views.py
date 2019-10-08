import datetime
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render
from scraping.models import *
from scraping.forms import FindVacancy
from scraping.utils import *


def home(request):
    form = FindVacancy
    return render(request, 'scraping/home.html', {'form': form})


def list_vacancy(request):
    today = datetime.date.today()
    form = FindVacancy
    context = {}
    if request.GET:
        form = FindVacancy(data=request.GET)
        if form.is_valid():
            print(form.cleaned_data)
            messages.success(request, 'Ok, action is right')
            qs = Vacancy.objects.filter(
                city=form.cleaned_data['city'],
                speciality=form.cleaned_data['speciality'],
                timestamp=today
            )
            if qs:
                context['form'] = form
                context['jobs'] = qs
                context['city'] = qs[0].city.name
                context['speciality'] = qs[1].speciality.name

                return render(request, 'scraping/list.html', context)
        else:
            print(form.errors)
            messages.error(request, 'Please, try again')

    return render(request, 'scraping/list.html',  {'form': form})

