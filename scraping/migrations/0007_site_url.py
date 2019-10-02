# Generated by Django 2.2.5 on 2019-10-01 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0006_auto_20191001_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='specialty')),
            ],
            options={
                'verbose_name': 'Site',
                'verbose_name_plural': 'Sites',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_address', models.CharField(max_length=50, verbose_name='url_address')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.City', verbose_name='city')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.Site', verbose_name='site')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.Specialty', verbose_name='speciality')),
            ],
            options={
                'verbose_name': 'Url',
                'verbose_name_plural': 'Urls',
            },
        ),
    ]