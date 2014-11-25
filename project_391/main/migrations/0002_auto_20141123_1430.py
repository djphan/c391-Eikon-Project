# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='user_name',
            field=models.ForeignKey(null=True, db_column='user_name', to='main.Users'),
        ),
    ]
