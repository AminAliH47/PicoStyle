# Generated by Django 3.2.9 on 2022-02-14 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20220212_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]
