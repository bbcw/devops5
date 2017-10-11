# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-17 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20170917_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=32, verbose_name='业务线的名字')),
                ('module_letter', models.CharField(db_index=True, max_length=10, verbose_name='业务线字母简称')),
                ('op_interface', models.CharField(max_length=150, verbose_name='运维对接人')),
                ('dev_interface', models.CharField(max_length=150, verbose_name='业务对接人')),
                ('pid', models.IntegerField(db_index=True, verbose_name='上级业务线id')),
            ],
        ),
    ]
