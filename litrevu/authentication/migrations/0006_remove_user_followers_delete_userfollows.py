# Generated by Django 4.2.5 on 2023-09-30 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_user_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.DeleteModel(
            name='UserFollows',
        ),
    ]
