# Generated by Django 2.2.4 on 2019-12-23 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('florence', '0002_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='0', max_length=120),
        ),
    ]
