# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-10-18 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_auto_20211018_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.TextField(default=''),
        ),
    ]
