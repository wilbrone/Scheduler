# Generated by Django 3.0.2 on 2020-01-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0005_event_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateField(default='2020-01-23'),
            preserve_default=False,
        ),
    ]
