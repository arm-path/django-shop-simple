from slugify import slugify
from django.db import models
from django.core.exceptions import ValidationError

from .functions import is_digit


class Category(models.Model):
    """ Модель категори """
    title = models.CharField('Название', max_length=154, unique=True)
    slug = models.SlugField('URL', max_length=154, blank=True, unique=True)

    def __str__(self):
        return self.title

    def clean(self):
        slug = slugify(self.title)
        if Category.objects.filter(slug=slug).exists():
            if not self.pk and not Category.objects.filter(pk=self.pk, slug=slug).exists():
                raise ValidationError('Категория с таким url уже существует!')
        self.slug = slug

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """ Модель продукта """
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL', max_length=255, blank=True, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField('Изображение', upload_to='products/%Y/', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2, default=0.00)
    product_availability = models.BooleanField('Наличие товара', default=True)
    description = models.TextField('Описание', blank=True, null=True)
    rating = models.FloatField('Рейтинг', default=0.0)
    specification = models.ManyToManyField('ValuesOfSpecification', blank=True, verbose_name='Характеристики')

    def __str__(self):
        return self.title

    def clean(self):
        slug = slugify(self.title)
        if Product.objects.filter(slug=slug).exists():
            if not self.pk and not Category.objects.filter(pk=self.pk, slug=slug).exists():
                raise ValidationError('Продукт с таким названием уже существует!')
        self.slug = slug

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Specification(models.Model):
    """ Модель спецификации """

    CUSTOM = 'custom'
    BASE = 'base'
    CHOICE_TYPE_FILTER = ((BASE, 'Основной'), (CUSTOM, 'Кастомный'))

    title = models.CharField('Название', max_length=154)
    slug = models.SlugField('URL', max_length=154, blank=True, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    unit = models.CharField('Ед. измерения', max_length=64, blank=True, null=True)
    use_filters = models.BooleanField('Использование в фильтрах', default=False)
    type_filter = models.CharField('Тип фильтра', max_length=64, choices=CHOICE_TYPE_FILTER, default=BASE)

    def __str__(self):
        return f'{self.category.title} - {self.title}'

    def clean(self):
        slug_string = f'{self.category.title}_{self.title}'
        slug = slugify(slug_string)
        if Specification.objects.filter(slug=slug).exists():
            if not self.pk and not Specification.objects.filter(pk=self.pk, slug=slug).exists():
                raise ValidationError('Характеристика с таким url уже существует!')
        self.slug = slug
        if self.type_filter == self.CUSTOM:
            if ValuesOfSpecification.objects.filter(specification=self):
                for obj in ValuesOfSpecification.objects.filter(specification=self):
                    if not is_digit(obj.value):
                        raise ValidationError(
                            'Перед изменения типа, убедитесь что значения характеристик являются числами!')

    class Meta:
        unique_together = ('title', 'category')
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class ValuesOfSpecification(models.Model):
    """ Модель возможных значений характеристик """
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE, related_name='values_sp', verbose_name='Характеристика')
    value = models.CharField('Значение', max_length=154)

    def __str__(self):
        return f'{self.specification.title}: {self.value} {self.specification.unit}'

    def clean(self):
        if self.specification.type_filter == 'custom':
            if not is_digit(self.value):
                raise ValidationError('Характеристика с кастомным типом, может иметь только числовые значения!')

    class Meta:
        unique_together = ('specification', 'value')
        verbose_name = 'Значение хакрктеристик'
        verbose_name_plural = 'Значения характеристик'


class CustomFilter(models.Model):
    """ Модель кастомных фильтров """
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE, related_name='one_filter', verbose_name='Характеристика')
    lessOrEqual = models.FloatField('Менее ( До )', blank=True, null=True)
    moreOrEqual = models.FloatField('Более ( От )', blank=True, null=True)

    def __str__(self):
        if self.lessOrEqual and self.moreOrEqual:
            return f'{self.specification.title} | Фильтры: Меньше или равно: {self.lessOrEqual}, Больше или равно: {self.moreOrEqual}'
        elif self.lessOrEqual:
            return f'{self.specification.title} | Фильтр: Меньше или равно: {self.lessOrEqual}'
        else:
            return f'{self.specification.title} | Фильтр: Больше или равно: {self.moreOrEqual}'

    def clean(self):
        if not self.lessOrEqual and not self.moreOrEqual:
            raise ValidationError('Должна быть заполнено, хотя бы одно поле "Меньше или равно" "Больше или равно"! ')
        if not self.specification.type_filter == 'custom':
            raise ValidationError('Выбранная характеристика должна бысть с кастомным типом фильтра!')
        if self.lessOrEqual and self.moreOrEqual:
            if self.moreOrEqual < 0 or self.lessOrEqual < 0:
                raise ValidationError('Возможны только положительные значения!')
            if self.lessOrEqual < self.moreOrEqual:
                raise ValidationError('Значение "больше или равно" не может быть больше значения "меньше или равно"')
        if self.lessOrEqual and not self.moreOrEqual:
            if CustomFilter.objects.filter(lessOrEqual=self.lessOrEqual).exists():
                if not self.pk and not CustomFilter.objects.filter(pk=self.pk, lessOrEqual=self.lessOrEqual).exists():
                    raise ValidationError('Данные уже существуют!')
            if self.lessOrEqual < 0:
                raise ValidationError('Возможны только положительные значения!')
        if self.moreOrEqual and not self.lessOrEqual:
            if CustomFilter.objects.filter(moreOrEqual=self.moreOrEqual).exists():
                if not self.pk and not CustomFilter.objects.filter(pk=self.pk, lessOrEqual=self.moreOrEqual).exists():
                    raise ValidationError('Данные уже существуют!')
            if self.moreOrEqual < 0:
                raise ValidationError('Возможны только положительные значения!')

    class Meta:
        unique_together = ('specification', 'lessOrEqual', 'moreOrEqual')
        verbose_name = 'Кастомный фильтр'
        verbose_name_plural = 'Кастомные фильтры'
