# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class_data',
            name='grades',
            field=models.TextField(default='[]', max_length=10000),
        ),
    ]