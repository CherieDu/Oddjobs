# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oddjobs', '0004_job_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.ImageField(default=b'profile-avatar/419.jpg', upload_to=b'profile-avatar'),
        ),
    ]
