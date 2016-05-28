# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150917_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('name', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
                ('visible', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
        migrations.AlterField(
            model_name='ticketorder',
            name='event',
            field=models.ForeignKey(related_name='orders', to='events.Event'),
        ),
        migrations.AddField(
            model_name='tickettype',
            name='event',
            field=models.ForeignKey(related_name='ticket_types', to='events.Event'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.ForeignKey(related_name='tickets', to='events.TicketType', null=True),
        ),
    ]
