# Generated by Django 4.2.17 on 2024-12-20 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='helpful',
            field=models.BooleanField(default=False),
        ),
    ]
