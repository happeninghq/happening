# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields
from django.conf import settings
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_auto_20150911_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('purchased_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='did_not_attend',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='last_edited_datetime',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='number',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='purchased_datetime',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='votes',
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
        migrations.AddField(
            model_name='ticket',
            name='order',
            field=models.ForeignKey(related_name='tickets', to='events.TicketOrder', null=True),
        ),
    ]
