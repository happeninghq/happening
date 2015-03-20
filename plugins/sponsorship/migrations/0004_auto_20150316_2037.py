# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0003_auto_20150311_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunitySponsorship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sponsor', models.ForeignKey(related_name='community_sponsorships', to='sponsorship.Sponsor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorTier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='communitysponsorship',
            name='tier',
            field=models.ForeignKey(related_name='community_sponsorships', to='sponsorship.SponsorTier'),
            preserve_default=True,
        ),
    ]
