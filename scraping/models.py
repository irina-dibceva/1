from django.db import models
from django.db.models.indexes import Index


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name= 'city')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Specialty(models.Model):
    name = models.CharField(max_length=50, verbose_name='specialty')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'


class Site(models.Model):
    name = models.CharField(max_length=50, verbose_name='site')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'


class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='city')
    speciality = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='speciality')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='site')
    url_address = models.CharField(max_length=250, verbose_name='url_address')

    def __str__(self):
        return self.url_address

    class Meta:
        verbose_name = 'Url'
        verbose_name_plural = 'Urls'


class Vacancy(models.Model):
    url_vacancy = models.CharField(max_length=250, unique=True, verbose_name='url')
    title = models.CharField(max_length=250, verbose_name='vacancy')
    description = models.TextField(blank=True, verbose_name='description vacancy')
    company = models.CharField(max_length=250, blank=True, verbose_name='name company')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='city')
    speciality = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='speciality')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'





