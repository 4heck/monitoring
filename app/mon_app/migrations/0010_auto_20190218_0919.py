# Generated by Django 2.1.5 on 2019-02-18 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mon_app', '0009_auto_20190217_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='categoryId',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID категории'),
        ),
        migrations.AlterField(
            model_name='item',
            name='groupId',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID группы'),
        ),
        migrations.AlterField(
            model_name='item',
            name='shop',
            field=models.CharField(blank=True, choices=[('Мвидео', 'Мвидео'), ('Ситилинк', 'Ситилинк'), ('Wildberries', 'Wildberries')], max_length=30, null=True, verbose_name='Магазин'),
        ),
    ]