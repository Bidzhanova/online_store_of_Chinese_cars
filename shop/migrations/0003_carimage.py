# Generated by Django 4.2.3 on 2023-07-10 17:43

from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=shop.models.car_images_directory_path, verbose_name='изображение')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='shop.car', verbose_name='автомобиль')),
            ],
            options={
                'verbose_name': 'изображение автомобиля',
                'verbose_name_plural': 'изображения автомобилей',
            },
        ),
    ]
