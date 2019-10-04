from django import forms
from scraping.models import City, Specialty
from .models import Subscriber


class SubscriberModelForm(forms.ModelForm):
    email = forms.EmailField(label='e-mail', required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    speciality = forms.ModelChoiceField(label='Specialty', queryset=Specialty.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Subscriber

        fields = ('email', 'city', 'speciality', 'password')
        exclude = {'is_active', }


class LoginForm(forms.Form):
    email = forms.EmailField(label='e-mail', required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            qs = Subscriber.objects.filter(email=email).first()
            if qs is None:
                raise forms.ValidationError('Not')
            elif password != qs.password:
                raise forms.ValidationError('Not')
        return email


class SubscriberEmailForm(forms.ModelForm):
    email = forms.EmailField(label='e-mail', required=True,
                             widget=forms.HiddenInput())
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    speciality = forms.ModelChoiceField(label='Specialty', queryset=Specialty.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(label='Get mail', required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Subscriber
        fields = ('email', 'city', 'speciality', 'password', 'is_active')



