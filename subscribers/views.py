from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import FormView, CreateView
from .forms import SubscriberModelForm
from .models import *


class SubscriberCreate(CreateView):
    model = Subscriber
    form_class = SubscriberModelForm
    template_name = 'subscribers/create.html'
    success_url = reverse_lazy('create')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, 'Ok, action is right')
            #user = Subscriber(city=city.id, speciality=speciality.id, url_vacancy=job['href'],
            #                  title=job['title'], description=job['descr'],
            #                  company=job['company'])
            #user.save()
            return self.form_valid(form)
        else:
            messages.error(request, 'Please, try again')
            return self.form_invalid(form)
