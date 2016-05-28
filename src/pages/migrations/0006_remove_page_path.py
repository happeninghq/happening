# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_page__data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='path',
        ),
    ]
