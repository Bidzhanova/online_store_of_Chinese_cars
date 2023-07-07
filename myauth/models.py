from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        ordering = ['user',]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    avatar = models.ImageField(blank=True, default='users/avatars/default.png',
                               upload_to=f'users/avatars/%Y/%m/%d/', validators=[
            FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg')),
    ], verbose_name='аватар')
    birth_date = models.DateField(null=True, blank=True, verbose_name='дата рождения')
    bio = models.TextField(max_length=500, blank=True, verbose_name='о себе')


    def __str__(self):
        return self.user.username
