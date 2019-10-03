"""find_work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.urls import path

from subscribers.views import SubscriberCreate, login_subscriber, update_subscriber
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/', home_list),
    path('list/', list_vacancy, name='list'),
    url(r'^create/', SubscriberCreate.as_view(), name='create'),
    path('update/', update_subscriber),
    path('login/', login_subscriber, name='login'),
    url(r'^', home),
]
