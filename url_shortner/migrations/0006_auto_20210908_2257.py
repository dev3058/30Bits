# Generated by Django 3.2.6 on 2021-09-08 17:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortner', '0005_alter_urllead_shortened_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urllead',
            name='id',
        ),
        migrations.AlterField(
            model_name='urllead',
            name='shortened_url',
            field=models.SlugField(default='BE933', primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(5)]),
        ),
    ]