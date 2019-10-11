from django.db import models
import uuid
from scraping.models import City, Specialty


class Subscriber(models.Model):
    email = models.CharField(max_length=150, unique=True, verbose_name='e-mail')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='city')
    speciality = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='speciality')
    password = models.CharField(max_length=150, verbose_name='password')
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True, verbose_name='is_active')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
