# Generated by Django 4.2.7 on 2023-12-30 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_mss_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cardUserKey',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
