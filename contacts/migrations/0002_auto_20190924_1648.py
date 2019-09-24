# Generated by Django 2.2.1 on 2019-09-24 08:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icl_contactmodel',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone Number must entered in the format:'+123456789'.Up to 12 digits allowed.", regex='^\\+?1?\\d{9,12}$')]),
        ),
        migrations.AlterField(
            model_name='icl_contactmodel',
            name='tel_number',
            field=models.CharField(blank=True, max_length=7, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Telephone Number is up to 7 digits allowed', regex='\\d{7}$')]),
        ),
    ]