# Generated by Django 4.2.13 on 2024-05-30 09:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='id',
        ),
        migrations.AddField(
            model_name='branch',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
