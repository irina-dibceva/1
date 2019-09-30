from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name= 'city')

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url_vacancy = models.CharField(max_length=250, unique=True, verbose_name='url')
    title = models.CharField(max_length=250, verbose_name='vacancy')
    description = models.TextField(blank=True, verbose_name='description vacancy')
    company = models.CharField(max_length=250, blank=True, verbose_name='name company')
    city = models.CharField(max_length=250, blank=True, verbose_name='city')
    speciality = models.CharField(max_length=250, blank=True, verbose_name='speciality')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title





