from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import FormView, CreateView
from .forms import SubscriberModelForm, LoginForm, SubscriberEmailForm
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
            return self.form_valid(form)
        else:
            messages.error(request, 'Please, try again')
            return self.form_invalid(form)


def login_subscriber(request):
    if request.method == 'GET':
        form = LoginForm
        return render(request, 'subscribers/login.html', {'form':form})
    elif request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            request.session['email'] = data['email']
            return redirect('update')

        return render(request, 'subscribers/login.html', {'form': form})


def update_subscriber(request):
    if request.method == 'GET' and request.session.get('email', False):
        email = request.session.get('email')
        qs = Subscriber.object.filter(email=email).first()

        form = SubscriberEmailForm(initial={'email': qs.email, 'city': qs.city,
                                            'speciality': qs.speciality, 'password': qs.password,
                                            'is_active': qs.is_active})
        return render(request, 'subscribers/update.html', {'form': form})
    elif request.method == 'POST':
        email = request.session.get('email')
        user = get_object_or_404(Subscriber, email=email)
        form = SubscriberEmailForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ok, action is right')
            del request.session['email']
            return redirect('list')
        messages.error(request, 'Please, try again')
        return render(request, 'subscribers/update.html', {'form': form})
    else:
        return redirect('login')

