# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20141111_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='photo',
            field=models.ImageField(upload_to='Images', max_length=250),
        ),
        migrations.AlterField(
            model_name='images',
            name='thumbnail',
            field=models.ImageField(upload_to='Thumbnails/', max_length=250),
        ),
    ]
