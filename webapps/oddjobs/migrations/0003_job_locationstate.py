# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oddjobs', '0002_comment_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='locationState',
            field=models.CharField(default=b'USA', max_length=200),
            preserve_default=True,
        ),
    ]
