# Generated by Django 2.1.5 on 2019-04-09 02:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginpage', '0006_auto_20190409_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='duration',
            field=models.PositiveSmallIntegerField(default=90, validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(30)]),
        ),
    ]
