from django.db import models


def brand_image_directory_path(instance: 'Brand', filename: str) -> str:
    return 'brands/{title}/image/{filename}'.format(
        title=instance.title,
        filename=filename
    )

def car_preview_directory_path(instance: 'Car', filename: str) -> str:
    return 'cars/{brand}/{model}/preview/{filename}'.format(
        brand=instance.brand,
        model=instance.model,
        filename=filename,
    )

def car_images_directory_path(instance: 'CarImage', filename: str) -> str:
    return 'cars/{brand}/{model}/images/{filename}'.format(
        brand=instance.car.brand,
        model=instance.car.model,
        filename=filename
    )


class Brand(models.Model):
    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'

    title = models.CharField(max_length=100, verbose_name='название')
    brand_country = models.CharField(max_length=30, default='Китай', verbose_name='страна бренда')
    description = models.TextField(blank=True, verbose_name='описание')
    image = models.ImageField(upload_to=brand_image_directory_path, blank=True, verbose_name='изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return self.title


class Car(models.Model):
    class Meta:
        verbose_name = 'автомобиль'
        verbose_name_plural = 'автомобили'

    CAR_CLASS_CHOICES = (
        ('A', 'a'),
        ('B', 'b'),
        ('C', 'c'),
        ('D', 'd'),
        ('E', 'e'),
        ('F', 'f'),
        ('S', 's'),
        ('M', 'm'),
        ('J', 'j'),
    )

    TRANSMISSION_CHOICES = (
        ('механика', 'Механика'),
        ('автомат', 'Автомат'),
        ('робот', 'Робот'),
        ('вариатор', 'Вариатор'),
    )

    DRIVE_CHOICES = (
        ('задний', 'Задний'),
        ('передний', 'Передний'),
        ('полный', 'Полный'),
    )

    price = models.DecimalField(max_digits=8, decimal_places=0, verbose_name='цена')
    discount = models.PositiveSmallIntegerField(default=0, verbose_name='скидка')
    preview = models.ImageField(blank=True, upload_to=car_preview_directory_path, verbose_name='превью')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brands', verbose_name='бренд')
    model = models.CharField(max_length=100, verbose_name='модель')
    car_class = models.CharField(max_length=1, choices=CAR_CLASS_CHOICES, verbose_name='класс автомобиля')
    doors_qty = models.PositiveSmallIntegerField(verbose_name='количество дверей')
    seats_qty = models.PositiveSmallIntegerField(verbose_name='количеств мест')
    transmission = models.CharField(max_length=8, choices=TRANSMISSION_CHOICES, verbose_name='коробка')
    engine_power = models.PositiveSmallIntegerField(verbose_name='мощность двигателя (л.с.)')
    engine_capacity = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='объём двигателя (л)')
    drive = models.CharField(max_length=8, choices=DRIVE_CHOICES, verbose_name='привод')
    consumption = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='расход')
    trunk_volume = models.PositiveSmallIntegerField(verbose_name='объём багажника (л)')
    fuel_tank_capacity = models.PositiveSmallIntegerField(verbose_name='объём топливного бака (л)')
    max_speed = models.PositiveSmallIntegerField(verbose_name='максимальная скорость (км/ч)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return f'{self.model}'


class CarImage(models.Model):
    class Meta:
        verbose_name = 'изображение автомобиля'
        verbose_name_plural = 'изображения автомобилей'

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars', verbose_name='автомобиль')
    image = models.ImageField(upload_to=car_images_directory_path, verbose_name='изображение')
    description = models.TextField(blank=True, verbose_name='описание')

    def __str__(self):
        return str(self.pk)
