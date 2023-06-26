# Generated by Django 4.2.1 on 2023-05-23 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('cal', models.FloatField()),
                ('sodium', models.FloatField()),
                ('sugar', models.FloatField()),
            ],
        ),
    ]
