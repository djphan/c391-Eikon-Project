# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouplists',
            name='friend_id',
            field=models.ForeignKey(db_column='friend_id', to='main.Users'),
        ),
        migrations.AlterField(
            model_name='grouplists',
            name='group_id',
            field=models.ForeignKey(db_column='group_id', to='main.Groups'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='group_name',
            field=models.CharField(db_column='group_name', max_length=24),
        ),
        migrations.AlterField(
            model_name='groups',
            name='user_name',
            field=models.ForeignKey(db_column='user_name', to='main.Users'),
        ),
        migrations.AlterField(
            model_name='images',
            name='owner_name',
            field=models.ForeignKey(db_column='owner_name', to='main.Users'),
        ),
        migrations.AlterField(
            model_name='images',
            name='permitted',
            field=models.ForeignKey(db_column='permitted', to='main.Groups'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='user_name',
            field=models.ForeignKey(primary_key=True, db_column='user_name', serialize=False, to='main.Users'),
        ),
    ]
