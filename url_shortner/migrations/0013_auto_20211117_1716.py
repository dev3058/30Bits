# Generated by Django 3.2.7 on 2021-11-17 11:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('url_shortner', '0012_alter_imagestorage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urllead',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='urllead',
            name='redirect_path',
            field=models.URLField(default='https://3058.in'),
        ),
        migrations.AlterField(
            model_name='urllead',
            name='shortened_url',
            field=models.SlugField(default='/', unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(20)]),
        ),
        migrations.AlterField(
            model_name='urllead',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
