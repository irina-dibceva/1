from django import forms
from .models import *


class FindVacancy(forms.Form):
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}))
    speciality = forms.ModelChoiceField(label='Specialty', queryset=Specialty.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}))

