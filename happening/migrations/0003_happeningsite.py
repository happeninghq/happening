# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('happening', '0002_configurationvariable__data'),
    ]

    operations = [
        migrations.CreateModel(
            name='HappeningSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
