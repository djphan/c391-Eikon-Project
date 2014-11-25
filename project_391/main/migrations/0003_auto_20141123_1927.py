# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20141123_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persons',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
