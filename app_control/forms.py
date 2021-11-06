from django import forms
from django.core.exceptions import ValidationError

from app_product.models import Category, Specification, ValuesOfSpecification


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
