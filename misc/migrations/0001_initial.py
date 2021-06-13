# Generated by Django 3.1.4 on 2021-06-01 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, unique=True)),
                ('answer', models.TextField()),
                ('slug', models.SlugField(default='', max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SlideShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_image', models.ImageField(upload_to='images/slide-show')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slider_sub_header', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(default='', max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
