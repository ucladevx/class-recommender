# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-15 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0005_home_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('sections', models.TextField(max_length=4000)),
                ('statuses', models.TextField(max_length=4000)),
                ('waitlists', models.TextField(max_length=4000)),
            ],
        ),
    ]
