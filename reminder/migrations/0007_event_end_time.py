# Generated by Django 3.0.2 on 2020-01-23 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0006_event_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='18:30:00'),
            preserve_default=False,
        ),
    ]
