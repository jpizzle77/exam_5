# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-18 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0003_auto_20171118_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(default=False, null=True),
        ),
    ]