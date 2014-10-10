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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('group_id', models.IntegerField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(db_column='group_name', max_length=24)),
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
                ('photo_id', models.IntegerField(primary_key=True, serialize=False)),
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
            name='Session',
            fields=[
                ('sessionid', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(db_column='user_name', primary_key=True, serialize=False, max_length=24)),
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
                ('user_name', models.ForeignKey(db_column='user_name', primary_key=True, to='main.Users', serialize=False)),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
                ('address', models.CharField(max_length=128)),
                ('email', models.CharField(unique=True, max_length=128)),
                ('phone', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'persons',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='session',
            name='username',
            field=models.ForeignKey(to='main.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='images',
            name='owner_name',
            field=models.ForeignKey(db_column='owner_name', to='main.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='images',
            name='permitted',
            field=models.ForeignKey(db_column='permitted', to='main.Groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groups',
            name='user_name',
            field=models.ForeignKey(db_column='user_name', to='main.Users'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='groups',
            unique_together=set([('user_name', 'group_name')]),
        ),
        migrations.AddField(
            model_name='grouplists',
            name='friend_id',
            field=models.ForeignKey(db_column='friend_id', to='main.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grouplists',
            name='group_id',
            field=models.ForeignKey(db_column='group_id', to='main.Groups'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='grouplists',
            unique_together=set([('group_id', 'friend_id')]),
        ),
    ]
