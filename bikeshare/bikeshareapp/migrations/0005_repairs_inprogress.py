# Generated by Django 3.1.5 on 2021-02-10 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikeshareapp', '0004_merge_20210209_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairs',
            name='InProgress',
            field=models.IntegerField(default=0),
        ),
    ]
