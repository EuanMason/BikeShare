# Generated by Django 3.1.5 on 2021-02-18 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bikeshareapp', '0007_auto_20210213_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('MovementID', models.AutoField(primary_key=True, serialize=False)),
                ('InProgress', models.IntegerField(default=0)),
                ('BikeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bikeshareapp.bike')),
                ('MoveOperator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='move_operator', to='bikeshareapp.user')),
                ('ProposedLocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposed_location', to='bikeshareapp.address')),
            ],
            options={
                'db_table': 'movement',
            },
        ),
    ]