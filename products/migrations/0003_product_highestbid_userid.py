# Generated by Django 3.1.3 on 2020-11-19 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_highestbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='highestbid_userid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
