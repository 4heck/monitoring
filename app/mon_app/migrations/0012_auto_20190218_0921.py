# Generated by Django 2.1.5 on 2019-02-18 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mon_app', '0011_auto_20190218_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='categoryId',
            field=models.SlugField(blank=True, max_length=300, null=True, verbose_name='ID категории'),
        ),
    ]
