# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20141110_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='group_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='sessiontracker',
            field=models.CharField(max_length=32, serialize=False, primary_key=True),
        ),
    ]
