# -*- coding: utf-8 -*-


from django.db import models, migrations
import django_pgjson.fields
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_pluginsetting__data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('started', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('complete_time', models.DateTimeField(null=True)),
                ('zip_file', models.FileField(null=True, upload_to=happening.storage.inner)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
