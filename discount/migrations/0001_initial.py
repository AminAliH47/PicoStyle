# Generated by Django 3.2.9 on 2022-02-12 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_discount', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(blank=True, limit_choices_to={'is_seller': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productscategory')),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': '02. Discount show/hide status',
            },
        ),
        migrations.CreateModel(
            name='Discounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wholesale_value', models.SmallIntegerField(default=0, help_text='%')),
                ('retail_value', models.SmallIntegerField(default=0, help_text='%')),
                ('all_products', models.BooleanField(default=False, verbose_name='Discount on all the products?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('accepted', 'accepted'), ('pending', 'pending'), ('rejected', 'rejected')], default='pending', max_length=10)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productscategory')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'discounts',
                'verbose_name_plural': '01. Discounts',
                'ordering': ('-created_at',),
            },
        ),
    ]
