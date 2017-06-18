from __future__ import unicode_literals
from django.db import migrations


def migrate_locations(apps, schema_editor):
    # {"city": "", "country": "", "longitude": "", "latitude": "", "state": "", "postcode": "", "line_1": "", "line_3": "", "line_2": ""}
    Event = apps.get_model('events', 'Event')
    for event in Event.objects.all():

        if event.location:
            if "city" in event.location:
                # Old style location
                fields = [
                    event.location[f] for f in ["line_1", "line_2", "line_3", "city", "state", "postcode", "country"] if event.location[f]
                ]
                longitude = event.location["longitude"]
                latitude = event.location["latitude"]
                event.location = {
                    "title": ", ".join(fields)
                }

                if longitude:
                    event.location["longitude"] = longitude
                    event.location["latitude"] = latitude

            event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20170422_1128'),
    ]

    operations = [
        migrations.RunPython(migrate_locations, migrations.RunPython.noop),
    ]
