# Generated by Django 2.2.3 on 2021-03-10 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_ents'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ents',
            old_name='entreli',
            new_name='entrele',
        ),
    ]