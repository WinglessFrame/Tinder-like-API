# Generated by Django 3.1.6 on 2021-02-18 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GinderApp', '0003_auto_20210216_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='search_distance',
            field=models.IntegerField(blank=True, default=20),
        ),
    ]
