# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('oddjobs', '0002_comment_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='id',
        ),
        migrations.AddField(
            model_name='job',
            name='locationState',
            field=models.CharField(default=b'USA', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'post-photos', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='cellphone',
            field=models.CharField(default=b'', max_length=42, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='firstname',
            field=models.CharField(default=b'', max_length=42, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='lastname',
            field=models.CharField(default=b'', max_length=42, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='location',
            field=models.CharField(default=b'', max_length=42, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
