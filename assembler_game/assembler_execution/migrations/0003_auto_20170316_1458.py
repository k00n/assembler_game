# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assembler_execution', '0002_auto_20170316_1428'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='expected_registers',
            new_name='expected_register_list',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='initial_registers',
            new_name='initial_register_list',
        ),
    ]
