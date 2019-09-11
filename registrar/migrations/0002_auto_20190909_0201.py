# Generated by Django 2.2.1 on 2019-09-08 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableCourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Course Category',
                'verbose_name_plural': 'Course Categories',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='availablecoursemodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registrar.AvailableCourseCategory'),
        ),
    ]
