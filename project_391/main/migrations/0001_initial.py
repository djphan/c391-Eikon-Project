# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupLists',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('notice', models.CharField(max_length=1024)),
            ],
            options={
                'db_table': 'group_lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('group_id', models.IntegerField(serialize=False, primary_key=True)),
                ('group_name', models.CharField(max_length=24)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('photo_id', models.IntegerField(serialize=False, primary_key=True)),
                ('subject', models.CharField(max_length=128)),
                ('place', models.CharField(max_length=128)),
                ('timing', models.DateField()),
                ('description', models.CharField(max_length=2048)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('photo', models.ImageField(upload_to='')),
            ],
            options={
                'db_table': 'images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_name', models.CharField(max_length=24, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=24)),
                ('date_registered', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('user_name', models.ForeignKey(to='main.Users', primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
                ('address', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128, unique=True)),
                ('phone', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'persons',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='images',
            name='owner_name',
            field=models.ForeignKey(to='main.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='images',
            name='permitted',
            field=models.ForeignKey(to='main.Groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groups',
            name='user_name',
            field=models.ForeignKey(to='main.Users'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='groups',
            unique_together=set([('user_name', 'group_name')]),
        ),
        migrations.AddField(
            model_name='grouplists',
            name='friend_id',
            field=models.ForeignKey(to='main.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grouplists',
            name='group_id',
            field=models.ForeignKey(to='main.Groups'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='grouplists',
            unique_together=set([('group_id', 'friend_id')]),
        ),
    ]
