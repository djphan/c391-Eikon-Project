# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20141009_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('sessionid', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.ForeignKey(to='main.Users')),
            ],
            options={
                'db_table': 'session',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='sessions',
            name='username',
        ),
        migrations.DeleteModel(
            name='Sessions',
        ),
    ]
