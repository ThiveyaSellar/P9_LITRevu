# Generated by Django 4.2.5 on 2023-11-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_review_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
