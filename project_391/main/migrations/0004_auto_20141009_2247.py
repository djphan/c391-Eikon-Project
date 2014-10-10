# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20141009_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='sessionid',
            new_name='sessiontracker',
        ),
    ]
