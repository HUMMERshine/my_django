# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
            ],
        ),
    ]