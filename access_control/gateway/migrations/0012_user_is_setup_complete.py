# Generated by Django 4.2.16 on 2024-10-19 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0011_alter_user_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_setup_complete',
            field=models.BooleanField(default=False),
        ),
    ]
