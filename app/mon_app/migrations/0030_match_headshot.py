# Generated by Django 2.1.5 on 2019-02-20 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mon_app', '0029_auto_20190219_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='headshot',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
