# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oddjobs', '0004_auto_20150422_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'post-photos', blank=True),
            preserve_default=True,
        ),
    ]
