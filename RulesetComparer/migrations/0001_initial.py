# Generated by Django 2.1.1 on 2018-12-19 08:00

from django.db import migrations
from RulesetComparer.services.initDataService import init_data


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('RulesetComparer', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_data),
    ]
