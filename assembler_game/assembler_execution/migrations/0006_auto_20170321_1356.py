# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 13:56
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assembler_execution', '0005_stage_registers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='registers',
            field=jsonfield.fields.JSONField(blank=True, default='{}'),
        ),
    ]
