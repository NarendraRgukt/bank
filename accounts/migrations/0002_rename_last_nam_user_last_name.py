# Generated by Django 4.2.13 on 2024-05-30 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_nam',
            new_name='last_name',
        ),
    ]
