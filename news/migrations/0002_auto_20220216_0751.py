# Generated by Django 3.2.9 on 2022-02-16 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorynews',
            name='title',
            field=models.CharField(help_text='Max length 20 character', max_length=20),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(help_text='Max length 30 character', max_length=30),
        ),
        migrations.AlterField(
            model_name='newstag',
            name='title',
            field=models.CharField(help_text='Max length 20 character', max_length=20),
        ),
    ]