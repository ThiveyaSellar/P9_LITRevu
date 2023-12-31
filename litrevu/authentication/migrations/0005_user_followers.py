# Generated by Django 4.2.5 on 2023-09-23 16:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_userfollows'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='following_users', through='authentication.UserFollows', to=settings.AUTH_USER_MODEL),
        ),
    ]
