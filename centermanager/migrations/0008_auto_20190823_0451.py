# Generated by Django 2.2.1 on 2019-08-22 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centermanager', '0007_auto_20190823_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='targetsheet',
            old_name='TargetSheet_ID',
            new_name='ts_id',
        ),
    ]
