# Generated by Django 4.2.16 on 2024-10-14 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0009_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
    ]