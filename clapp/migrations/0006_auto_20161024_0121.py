# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-24 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sixerrapp', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
