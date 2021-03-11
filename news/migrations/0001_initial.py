# Generated by Django 2.2.3 on 2021-02-15 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsurl', models.URLField(default='', max_length=255)),
                ('language', models.CharField(default='', max_length=3)),
                ('text_characters', models.IntegerField(default=0)),
                ('cat1', models.CharField(default='', max_length=255)),
                ('cat1_score', models.FloatField(default=0.0)),
                ('sentiment', models.CharField(default='', max_length=255)),
                ('senti_score', models.FloatField(default=0.0)),
                ('sadness', models.FloatField(default=0.0)),
                ('joy', models.FloatField(default=0.0)),
                ('fear', models.FloatField(default=0.0)),
                ('disgust', models.FloatField(default=0.0)),
                ('anger', models.FloatField(default=0.0)),
            ],
        ),
    ]
