# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oddjobs', '0007_auto_20150429_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='firstname',
            field=models.CharField(default=b'Anonymous', max_length=42, blank=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='lastname',
            field=models.CharField(default=b'Anonymous', max_length=42, blank=True),
        ),
    ]
