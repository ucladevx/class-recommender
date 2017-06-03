# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-15 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0006_section_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_data',
            name='abbrev',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='home_data',
            name='abbrev',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='home_data',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='home_data',
            name='subject',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='section_data',
            name='course',
            field=models.CharField(max_length=200),
        ),
    ]