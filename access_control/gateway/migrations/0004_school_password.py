# Generated by Django 4.2.16 on 2024-10-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0003_delete_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='password',
            field=models.CharField(default=123456789, max_length=128),
            preserve_default=False,
        ),
    ]
