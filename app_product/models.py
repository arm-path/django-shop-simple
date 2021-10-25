from django.db import models


class Category(models.Model):
    """ Модель категори """
    title = models.CharField('Название', max_length=154, unique=True)
    slug = models.SlugField('URL', max_length=154, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """ Модель продукта """
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField('Изображение', upload_to='products/%Y/', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2, default=0.00)
    product_availability = models.BooleanField('Наличие товара', default=True)
    description = models.TextField('Описание', blank=True, null=True)
    rating = models.FloatField('Рейтинг', default=0.0)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Specification(models.Model):
    """ Модель спецификации """

    CUSTOM = 'custom'
    BASE = 'base'
    CHOICE_TYPE_FILTER = ( (CUSTOM, 'Катомный'), (BASE, 'Основной') )

    title = models.CharField('Название', max_length=154)
    slug = models.SlugField('URL', max_length=154, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    unit = models.CharField('Ед. измерения', max_length=64, blank=True, null=True)
    use_filters = models.BooleanField('Использование в фильтрах', default=False)
    type_filter = models.CharField('Тип фильтра', max_length=64, choices=CHOICE_TYPE_FILTER, default=BASE)

    def __str__(self):
        return f'{self.category.title} | {self.title}'
    
    # TODO: Метод SAVE. 
    # 1. Построить slug, перед сохранением.
    # 2. Ограничить возможность изменения поля type_filter=custom, если значения характеристик, имеют значения, не являющиеся числом.
    
    class Meta:
        unique_together = ['title', 'category']
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class ValuesOfSpecification(models.Model):
    """ Модель возможных значений характеристик """
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE, verbose_name='Характеристика')
    value = models.CharField('Значение', max_length=154)
    products = models.ManyToManyField('Product', verbose_name='Продукты')

    def __str__(self):
        return f'{self.specification.title}: {self.value} {self.specification.unit}'
    
    # TODO: Метод SAVE. Значение может принимать только число, если specification.type_filter = custom.
    
    class Meta:
        unique_together = ['specification', 'value']
        verbose_name = 'Значение хакрктеристики'
        verbsoe_name_plural = 'Значения характеристики'


class CustomFilterOne(models.Model):
    """ Модель кастомных фильтров №1 """
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE, verbose_name='Характеристика')
    lessOrEqual = models.FloatField('Меньше или равно', blank=True, null=True)
    moreOrEqual = models.FloatField('Больше или равно', blank=True, null=True)

    def __str__(self):
        if self.lessOrEqual and moreOrEqual:
            return f'{self.specification.title} | Фильтры: Меньше или равно: {self.lessOrEqual}, Больше или равно: {self.moreOrEqual}'
        elif self.lessOrEqual:
            return f'{self.specification.title} | Фильтр: Меньше или равно: {self.lessOrEqual}'
        else:
            return f'{self.specification.title} | Фильтр: Больше или равно: {self.moreOrEqual}'
    
    # TODO: Метод SAVE. Проверять перед сохранением заполнение одного из полей: LessOrEqual or MoreOrEqual
    
    class Meta:
        verbose_name = 'Кастомный фильтр №1'
        verbose_name_plural = 'Кастомные фильтры №1'


class CustomFilterTwo(models.Model):
    """ Модель кастомных фильтров №2 """
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE, verbose_name='Характеристика')
    from_digit = models.FloatField('От')
    before_digit = models.FloatField('До')

    def __str__(self):
        return f'{self.specification.title} | Фильтр: От {self.from_digit} до {self.before_digit}'
    
    class Meta:
        verbose_name = 'Кастомный фильтр №2'
        verbose_name_plural = 'Кастомные фильтры №2'