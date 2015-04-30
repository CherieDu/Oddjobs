# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oddjobs', '0008_auto_20150430_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='title',
            field=models.CharField(default='default Title', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job',
            name='content',
            field=models.CharField(max_length=1000),
        ),
    ]
