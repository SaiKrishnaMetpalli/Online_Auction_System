# Generated by Django 3.1.3 on 2020-11-18 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('userid', models.IntegerField(blank=True, null=True)),
                ('winnerid', models.IntegerField(blank=True, null=True)),
                ('productname', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/images/')),
                ('endtime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]