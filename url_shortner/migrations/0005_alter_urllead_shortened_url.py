# Generated by Django 3.2.6 on 2021-09-08 16:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortner', '0004_alter_urllead_shortened_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urllead',
            name='shortened_url',
            field=models.SlugField(default='5F572', unique=True, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(5)]),
        ),
    ]
