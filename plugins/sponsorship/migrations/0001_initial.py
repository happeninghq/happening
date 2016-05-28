# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20160128_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(related_name='event_sponsors', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('logo', models.ImageField(upload_to=b'sponsors')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventsponsor',
            name='sponsor',
            field=models.ForeignKey(related_name='event_sponsors', to='sponsorship.Sponsor'),
            preserve_default=True,
        ),
    ]
