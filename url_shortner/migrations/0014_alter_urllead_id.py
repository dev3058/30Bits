# Generated by Django 3.2.7 on 2021-11-17 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortner', '0013_auto_20211117_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urllead',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]