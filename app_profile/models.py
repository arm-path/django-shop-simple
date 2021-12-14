from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """ Модель покупателя """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='customer', blank=True, null=True)
    date_of_birth = models.DateField('Дата рождения', auto_now=False, auto_now_add=False, blank=True, null=True)
    image_profile = models.ImageField('Изображение профиля', upload_to='profile/', blank=True, null=True)
    telephone = models.CharField('Телефон', max_length=18, blank=True, null=True)
    address = models.CharField('Адрес', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
