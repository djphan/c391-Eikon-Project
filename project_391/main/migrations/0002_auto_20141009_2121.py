# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('sessionid', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.ForeignKey(to='main.Users')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='session',
            name='username',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
