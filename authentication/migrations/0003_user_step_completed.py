# Generated by Django 5.1 on 2024-08-14 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='step_completed',
            field=models.BooleanField(default=False),
        ),
    ]
