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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('notice', models.CharField(max_length=1024, blank=True)),
            ],
            options={
                'verbose_name': 'GroupList',
                'db_table': 'group_lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('group_id', models.AutoField(serialize=False, primary_key=True)),
                ('group_name', models.CharField(db_column='group_name', max_length=24)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Group',
                'db_table': 'groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('photo_id', models.AutoField(serialize=False, primary_key=True)),
                ('subject', models.CharField(null=True, max_length=128, blank=True)),
                ('place', models.CharField(null=True, max_length=128, blank=True)),
                ('timing', models.DateField(null=True, blank=True)),
                ('description', models.CharField(null=True, max_length=2048, blank=True)),
                ('thumbnail', models.ImageField(upload_to='Thumbnails/', max_length=250)),
                ('photo', models.ImageField(upload_to='Images', max_length=250)),
            ],
            options={
                'verbose_name': 'Image',
                'db_table': 'images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('sessiontracker', models.CharField(serialize=False, max_length=32, primary_key=True)),
            ],
            options={
                'db_table': 'session',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectDashboard',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(serialize=False, db_column='user_name', max_length=24, primary_key=True)),
                ('password', models.CharField(max_length=24)),
                ('date_registered', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'User',
                'db_table': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('user_name', models.ForeignKey(serialize=False, db_column='user_name', primary_key=True, to='main.Users')),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
                ('address', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128, unique=True)),
                ('phone', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Person',
                'db_table': 'persons',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('photo_id', models.ForeignKey(db_column='photo_id', to='main.Images')),
                ('user_name', models.ForeignKey(db_column='user_name', to='main.Users')),
            ],
            options={
                'verbose_name': 'View',
                'db_table': 'views',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='views',
            unique_together=set([('photo_id', 'user_name')]),
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
