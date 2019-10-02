from django.contrib import admin

from .models import Subscriber


class SubAdmin(admin.ModelAdmin):
    class Meta:
        model = Subscriber
    list_display = ('email', 'city', 'speciality', 'is_active')
    list_editable = ['is_active']


admin.site.register(Subscriber, SubAdmin)
