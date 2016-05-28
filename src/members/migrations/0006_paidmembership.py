# -*- coding: utf-8 -*-


from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0005_auto_20141231_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaidMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_made', models.DateTimeField()),
                ('expiry_time', models.DateTimeField()),
                ('amount', models.IntegerField()),
                ('receipt', jsonfield.fields.JSONField(default=dict)),
                ('user', models.ForeignKey(related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
