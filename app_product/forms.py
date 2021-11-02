from django import forms

from .models import Category, Specification, ValuesOfSpecification


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

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Характеристика'
        self.fields['unit'].label = 'Ед. Измерения'
        self.fields['use_filters'].label = 'Использовать в фильтрах'
        self.fields['type_filter'].label = 'Тип фильтра'

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_title_specification'}))
    unit = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    use_filters = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input d-block'}))
    type_filter = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Specification.CHOICE_TYPE_FILTER)

    class Meta:
        model = Specification
        fields = ('title', 'unit', 'use_filters', 'type_filter')


class ValuesOfSpecificationForm(forms.ModelForm):
    """ Форма Значений характеристик """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].label = 'Значение'

    value = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ValuesOfSpecification
        fields = ('value',)
