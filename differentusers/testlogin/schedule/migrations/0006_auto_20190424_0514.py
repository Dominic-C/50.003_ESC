# Generated by Django 2.1.5 on 2019-04-24 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20190424_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='location',
            field=models.IntegerField(),
        ),
    ]
