# Generated by Django 5.1.7 on 2025-03-20 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_purchase_menu_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.FloatField(default=0),
        ),
    ]
