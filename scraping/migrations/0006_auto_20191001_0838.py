# Generated by Django 2.2.5 on 2019-10-01 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0005_auto_20191001_0824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='specialty')),
            ],
            options={
                'verbose_name': 'Specialty',
                'verbose_name_plural': 'Specialties',
            },
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'City', 'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.Specialty', verbose_name='speciality'),
        ),
    ]
