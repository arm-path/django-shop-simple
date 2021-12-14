import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import ValidationError

from .models import Customer


class CreateUserForm(UserCreationForm):
    """ Форма создания пользователя """

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control mb-2'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control mb-2'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    last_name = forms.CharField(label='Фамилие', widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 3:
            raise ValidationError('Укажите Ваше имя, минимальное допустимое количество символов: 3')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 3:
            raise ValidationError('Укажите Вашу фамилию, минимальное допустимое количество символов: 3')
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Указанный Email уже зарегистрирован в системе.')
        return email


class ChangeUserForm(forms.ModelForm):
    """ Форма изменения пользователя """

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    last_name = forms.CharField(label='Фамилие', widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CreateCustomerForm(forms.ModelForm):
    """ Форма создания покупателя - Расширение формы создания пользователя """

    date_of_birth = forms.DateField(label='Дата рождения',
                                    widget=forms.DateInput(attrs={'class': 'form-control mb-2', 'type': 'date'}, format='%Y-%m-%d'),
                                    required=False)
    image_profile = forms.ImageField(label='Изображение', widget=forms.FileInput(attrs={'class': 'form-control mb-2'}), required=False)
    telephone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    address = forms.CharField(label='Адрес', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        result = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', telephone)
        if not bool(result):
            raise ValidationError('Не правильно указан номер телефона.')
        return telephone

    class Meta:
        model = Customer
        fields = ('date_of_birth', 'image_profile', 'telephone', 'address')


class AuthenticationUserForm(AuthenticationForm):
    """ Форма авториации пользователя-покупателя """

    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
