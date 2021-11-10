from django import forms
from django.core.exceptions import ValidationError
from django.forms.fields import CharField

from app_product.models import Category, Specification, ValuesOfSpecification, Product


class CategoryForm(forms.ModelForm):
    """ Форма Категории """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = ('title',)


class SpecificationForm(forms.ModelForm):
    """ Форма Характеристик """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Характеристика'
        self.fields['unit'].label = 'Ед. Измерения'
        self.fields['use_filters'].label = 'Использовать в фильтрах'
        self.fields['type_filter'].label = 'Тип фильтра'

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_title_specification'}))
    category = forms.ModelChoiceField(
        widget=forms.HiddenInput(attrs={'style': 'form-control'}), queryset=Category.objects.all())
    unit = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}), required=False)
    use_filters = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input d-block', 'required': False}), required=False)
    type_filter = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}), choices=Specification.CHOICE_TYPE_FILTER)

    def category_clean(self):
        if not self.category:
            raise ValidationError('Укажите категорию характеристики!')

    def title_clean(self):
        if not self.title:
            raise ValidationError('Укажите название характеристики!')

    class Meta:
        model = Specification
        fields = ('title', 'category', 'unit', 'use_filters', 'type_filter')


class ValuesOfSpecificationForm(forms.ModelForm):
    """ Форма Значений характеристик """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].label = 'Значение'

    specification = forms.ModelChoiceField(
        widget=forms.HiddenInput(attrs={'style': 'form-control'}), queryset=Specification.objects.all())
    value = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ValuesOfSpecification
        fields = ('value', 'specification')


class ProductForm(forms.ModelForm):
    """ Форма Продукта """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'
        self.fields['category'].label = 'Категория'
        self.fields['image'].label = 'Изображение'
        self.fields['price'].label = 'Цена'
        self.fields['product_availability'].label = 'Наличие товара'
        self.fields['description'].label = 'Описание'

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        widget=forms.HiddenInput(attrs={'class': 'form-control'}), queryset=Category.objects.all())
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_availability = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input d-block', 'required': False}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Product
        fields = ('title', 'category', 'image', 'price', 'product_availability', 'description')
