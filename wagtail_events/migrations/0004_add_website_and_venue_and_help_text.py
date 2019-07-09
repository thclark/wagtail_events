# Generated by Django 2.1.4 on 2019-06-12 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_events', '0003_alter_event_index_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_website',
            field=models.URLField(blank=True, help_text='Optional external link for the event or programme', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.TextField(blank=True, help_text='The event venue', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='venue_website',
            field=models.URLField(blank=True, help_text='Link to the venue (or, say, a google maps pin)', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(blank=True, help_text='Event end time', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(help_text='Event start time'),
        ),
    ]