# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Jcrontab', '0002_auto_20200109_0940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demandorder',
            old_name='command_con',
            new_name='command',
        ),
    ]
