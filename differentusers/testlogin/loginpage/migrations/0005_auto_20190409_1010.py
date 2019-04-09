# Generated by Django 2.1.5 on 2019-04-09 02:10

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('loginpage', '0004_auto_20190408_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('pillar', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=20)),
                ('class_enrolled', models.CharField(max_length=10)),
                ('day_of_week', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('duration', models.PositiveSmallIntegerField(default=90, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(360)])),
            ],
        ),
        migrations.DeleteModel(
            name='Example',
        ),
    ]
