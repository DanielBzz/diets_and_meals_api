# Generated by Django 4.1.7 on 2023-05-31 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
