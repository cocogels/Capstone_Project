# Generated by Django 2.2.1 on 2019-09-25 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email Address')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(blank=True, max_length=50, verbose_name='Address')),
                ('is_centermanager', models.BooleanField(default=False, verbose_name='CenterManagerStatus')),
                ('is_centerbusinessmanager', models.BooleanField(default=False, verbose_name='CBM_Status')),
                ('is_marketinghead', models.BooleanField(default=False, verbose_name='MarketingHeadStatus')),
                ('is_registrar', models.BooleanField(default=False, verbose_name='Registrar Status')),
                ('is_budgetary', models.BooleanField(default=False, verbose_name='BUDGETARY')),
                ('is_ihe', models.BooleanField(default=False, verbose_name='IHE')),
                ('is_shs', models.BooleanField(default=False, verbose_name='SHS')),
                ('is_icl', models.BooleanField(default=False, verbose_name='ICL')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-is_active'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_no', models.BigIntegerField(null=True)),
                ('birth_date', models.DateField(max_length=100)),
                ('activation_key', models.CharField(max_length=50)),
                ('key_expires', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
