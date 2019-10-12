# Generated by Django 2.2.1 on 2019-10-11 16:40

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collateral',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('unit', models.CharField(max_length=255, null=True)),
                ('quantity', models.BigIntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
            ],
            options={
                'verbose_name_plural': 'Collateral',
            },
        ),
        migrations.CreateModel(
            name='SchoolDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('start_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('end_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('show_reports', models.BooleanField(default=True)),
                ('school_days', models.BooleanField(blank=True, default=False, help_text='if set this will ne the number of school days is in session. if unset, the value is calculated by the days off.', null=True)),
                ('monday', models.BooleanField(default=True)),
                ('tuesday', models.BooleanField(default=True)),
                ('wenesday', models.BooleanField(default=True)),
                ('thursday', models.BooleanField(default=True)),
                ('friday', models.BooleanField(default=True)),
                ('saturday', models.BooleanField(default=False)),
                ('sunday', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('b_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.BigIntegerField(null=True)),
                ('arrival', models.DateField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Budget',
            },
        ),
        migrations.CreateModel(
            name='AssignTerritory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('territory_choices', models.CharField(choices=[(1, 'DISTRICT I'), (2, 'DISTRICT II'), (3, 'DISTRICT III'), (4, 'DISTRICT IV'), (5, 'DISTRICT V'), (6, 'DISTRICT VI')], max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('assigned_to', models.ManyToManyField(related_name='assign_territory_user', to=settings.AUTH_USER_MODEL)),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='AssignQuota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_month', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('end_month', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('a_senior_high', models.BigIntegerField(null=True)),
                ('a_higher_education', models.BigIntegerField(null=True)),
                ('a_retail', models.BigIntegerField(null=True)),
                ('a_corporate', models.BigIntegerField(null=True)),
                ('a_owwa', models.BigIntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('assigned_to', models.ManyToManyField(related_name='assign_user', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assign_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
