# Generated by Django 4.2.16 on 2024-10-14 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0008_alter_user_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
