# Generated by Django 2.1.5 on 2019-02-18 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mon_app', '0022_auto_20190218_2347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='shop',
            new_name='shop_competitor',
        ),
    ]