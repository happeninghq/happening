# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationpreference',
            name='user',
            field=models.ForeignKey(related_name='notification_preferences', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
