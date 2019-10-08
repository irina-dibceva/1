import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import FormView, CreateView
from .forms import SubscriberModelForm, LoginForm, SubscriberEmailForm, ContactForm
from .models import *


ADMIN_EMAIL = settings.ADMIN_EMAIL
MAILGUN_KEY = settings.MAILGUN_KEY
API = settings.API
MAIL_SERVER = settings.MAIL_SERVER
PASSWORD_AWARD = settings.PASSWORD_AWARD
USER_AWARD = settings.USER_AWARD
FROM_EMAIL = settings.FROM_EMAIL


class SubscriberCreate(CreateView):
    model = Subscriber
    form_class = SubscriberModelForm
    template_name = 'subscribers/create.html'
    success_url = reverse_lazy('create')

    def post(self, request, *args, **kwargs):
        # form_class = self.get_form_class()
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Ok, action is right')
            return self.form_valid(form)
            #return redirect('admin')
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


def contact_admin(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            city = form.cleaned_data['city']
            speciality = form.cleaned_data['speciality']
            from_email = form.cleaned_data['email']
            content = 'Прошу добавить в поиск : город - {}'.format(city)
            content += ', специальность - {}'.format(speciality)
            content += 'Запрос от пользователя  {}'.format(from_email)
            # Subject = 'Запрос на добавление в БД'
            msg = MIMEMultipart()
            msg['Subject'] = 'Запрос на добавление в БД'
            msg['From'] = '<{email}>'.format(email=FROM_EMAIL)
            msg['To'] = ADMIN_EMAIL
            mail = smtplib.SMTP()
            mail.connect(MAIL_SERVER, 25)
            mail.ehlo()
            mail.starttls()
            mail.login(USER_AWARD, PASSWORD_AWARD)
            email = [ADMIN_EMAIL]
            msg.attach(MIMEText(content))
            mail.sendmail(FROM_EMAIL, email, msg.as_string())
            # requests.post(API,  auth=("api", MAILGUN_KEY), data={"from": from_email, "to": ADMIN_EMAIL,
            #                     "subject":Subject , "text": content})
            messages.success(request, 'Ваше письмо отправленно')
            mail.quit()
            return redirect('index')
        return render(request, 'subscribers/contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'subscribers/contact.html', {'form': form})
