# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchv1', '0003_auto_20161229_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.CharField(max_length=255),
        ),
    ]