# Generated by Django 3.2.9 on 2022-02-12 08:44

import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrandsSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('All', 'All'), ('Women', 'Women'), ('Men', 'Men'), ('Raw material', 'Raw material'), ('Life style', 'Life style')], help_text='Which home page to display?', max_length=15)),
                ('title_en', models.CharField(blank=True, max_length=15, verbose_name='Title')),
                ('title_ru', models.CharField(blank=True, max_length=15, verbose_name='Title')),
                ('title_it', models.CharField(blank=True, max_length=15, verbose_name='Title')),
                ('link', models.CharField(max_length=120)),
                ('description_en', models.TextField(blank=True, max_length=100, null=True, verbose_name='Description')),
                ('description_ru', models.TextField(blank=True, max_length=100, null=True, verbose_name='Description')),
                ('description_it', models.TextField(blank=True, max_length=100, null=True, verbose_name='Description')),
                ('button_en', models.CharField(blank=True, max_length=15, null=True, verbose_name='Button')),
                ('button_ru', models.CharField(blank=True, max_length=15, null=True, verbose_name='Button')),
                ('button_it', models.CharField(blank=True, max_length=15, null=True, verbose_name='Button')),
                ('button_link', models.CharField(blank=True, max_length=150, null=True)),
                ('cover', models.BooleanField(default=True, help_text='Have dark cover?')),
                ('image', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'slide',
                'verbose_name_plural': '03. Brands slider',
            },
        ),
        migrations.CreateModel(
            name='MainCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('All', 'All'), ('Women', 'Women'), ('Men', 'Men'), ('Raw material', 'Raw material'), ('Life style', 'Life style')], help_text='Which home page to display?', max_length=15)),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('image', models.ImageField(upload_to='main/categories')),
                ('link', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': '07. Main categories',
            },
        ),
        migrations.CreateModel(
            name='MainNavbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('All', 'All'), ('Women', 'Women'), ('Men', 'Men'), ('Raw material', 'Raw material'), ('Life style', 'Life style')], help_text='Which home page to display?', max_length=15)),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('slug', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': '04. Main navbar',
            },
        ),
        migrations.CreateModel(
            name='MainSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('All', 'All'), ('Women', 'Women'), ('Men', 'Men'), ('Raw material', 'Raw material'), ('Life style', 'Life style')], help_text='Which home page to display?', max_length=15)),
                ('title_en', models.CharField(blank=True, max_length=15, verbose_name='Title')),
                ('title_ru', models.CharField(blank=True, max_length=15, verbose_name='Title')),
                ('title_it', models.CharField(blank=True, max_length=15, verbose_name='Title')),
                ('link', models.CharField(max_length=120)),
                ('description_en', models.TextField(blank=True, max_length=120, null=True, verbose_name='Description')),
                ('description_ru', models.TextField(blank=True, max_length=120, null=True, verbose_name='Description')),
                ('description_it', models.TextField(blank=True, max_length=120, null=True, verbose_name='Description')),
                ('button_en', models.CharField(blank=True, max_length=15, null=True, verbose_name='Button')),
                ('button_ru', models.CharField(blank=True, max_length=15, null=True, verbose_name='Button')),
                ('button_it', models.CharField(blank=True, max_length=15, null=True, verbose_name='Button')),
                ('button_link', models.CharField(blank=True, max_length=150, null=True)),
                ('cover', models.BooleanField(default=True, help_text='Have dark cover?')),
                ('image', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'slide',
                'verbose_name_plural': '02. Main slider',
            },
        ),
        migrations.CreateModel(
            name='Retailers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('MS.', 'MS.'), ('MrS.', 'MrS.'), ('Mr.', 'Mr.')], max_length=4)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Your entered phone number is not valid', regex='^[ 0-9]+$')])),
                ('address', models.TextField()),
                ('zip_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('experience', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=4)),
                ('experience_info', models.JSONField()),
                ('have_store', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=4, null=True)),
                ('center_town', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=4, null=True)),
            ],
            options={
                'verbose_name': 'retailer',
                'verbose_name_plural': '08. Retailers',
            },
        ),
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='main/logo')),
                ('favicon', models.ImageField(upload_to='main/favicon')),
            ],
            options={
                'verbose_name': 'setting',
                'verbose_name_plural': '01. Site setting',
            },
        ),
        migrations.CreateModel(
            name='SizeGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=100, verbose_name='title')),
                ('title_ru', models.CharField(max_length=100, verbose_name='title')),
                ('title_it', models.CharField(max_length=100, verbose_name='title')),
                ('link', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to='main/size-guide')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': '12. Size guide',
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('title_ru', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('link', models.CharField(max_length=120)),
                ('icon_code', models.CharField(choices=[('linkedin', 'linkedin'), ('youtube', 'youtube'), ('facebook', 'facebook'), ('instagram', 'instagram'), ('telegram', 'telegram')], max_length=15)),
            ],
            options={
                'verbose_name': 'social media',
                'verbose_name_plural': '06. Social media',
            },
        ),
        migrations.CreateModel(
            name='SpecialProjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=100, verbose_name='title')),
                ('title_ru', models.CharField(max_length=100, verbose_name='title')),
                ('title_it', models.CharField(max_length=100, verbose_name='title')),
                ('link', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to='main/special-project')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': '10. Special projects',
            },
        ),
        migrations.CreateModel(
            name='StoreAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=120, null=True, verbose_name='Name')),
                ('name_ru', models.CharField(max_length=120, null=True, verbose_name='Name')),
                ('name_it', models.CharField(max_length=120, null=True, verbose_name='Name')),
                ('country', models.CharField(max_length=120)),
                ('country_code', models.CharField(max_length=4)),
                ('description_en', ckeditor.fields.RichTextField(max_length=450, null=True, verbose_name='Description')),
                ('description_ru', ckeditor.fields.RichTextField(max_length=450, null=True, verbose_name='Description')),
                ('description_it', ckeditor.fields.RichTextField(max_length=450, null=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='main/store-and-agent')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'store',
                'verbose_name_plural': '09. Store and agent',
            },
        ),
        migrations.CreateModel(
            name='SubNavbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('All', 'All'), ('Women', 'Women'), ('Men', 'Men'), ('Raw material', 'Raw material'), ('Life style', 'Life style')], help_text='Which home page to display?', max_length=15)),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('slug', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': '05. Sub navbar',
            },
        ),
        migrations.CreateModel(
            name='WorkWithUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=100, verbose_name='title')),
                ('title_ru', models.CharField(max_length=100, verbose_name='title')),
                ('title_it', models.CharField(max_length=100, verbose_name='title')),
                ('link', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to='main/work-with-us')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': '11. Work with us',
            },
        ),
    ]
