# Generated by Django 2.2.4 on 2020-02-07 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('credit', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lib',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('version', models.FloatField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('keywords', models.TextField(blank=True, max_length=500, null=True)),
                ('credit', models.IntegerField(default=0)),
                ('nlike', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExtLib',
            fields=[
                ('lib_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='florence.Lib')),
                ('url', models.URLField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
            bases=('florence.lib',),
        ),
        migrations.CreateModel(
            name='IntLib',
            fields=[
                ('lib_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='florence.Lib')),
                ('published', models.BooleanField(default=False)),
                ('code', models.TextField()),
                ('exports', models.TextField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('florence.lib',),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('credit', models.IntegerField(default=0)),
                ('nlike', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('keywords', models.TextField(blank=True, max_length=500, null=True)),
                ('published', models.BooleanField(default=False)),
                ('code', models.TextField()),
                ('exports', models.TextField(blank=True, max_length=500, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('alias', models.CharField(blank=True, max_length=100, null=True)),
                ('lib', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='florence.Lib')),
                ('on', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imports', to='florence.Lib')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
