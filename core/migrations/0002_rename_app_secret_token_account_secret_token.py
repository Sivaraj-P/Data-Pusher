# Generated by Django 5.1.2 on 2024-10-22 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='app_secret_token',
            new_name='secret_token',
        ),
    ]