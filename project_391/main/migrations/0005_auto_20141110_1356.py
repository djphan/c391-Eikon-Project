# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20141009_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='photo',
            field=models.ImageField(upload_to='Images'),
        ),
        migrations.AlterField(
            model_name='images',
            name='thumbnail',
            field=models.ImageField(upload_to='Thumbnails/'),
        ),
    ]
