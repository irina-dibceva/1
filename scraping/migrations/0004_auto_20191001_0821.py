# Generated by Django 2.2.5 on 2019-10-01 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_auto_20191001_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.CharField(max_length=250, verbose_name='city'),
        ),
    ]